from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa
from persistence.configuracao_repository import ConfiguracaoRepository


class Relatorio:
    """Gera relatórios a partir dos lançamentos financeiros."""

    def __init__(self, lancamentos):
        self.lancamentos = lancamentos
        self.configuracao = ConfiguracaoRepository().carregar()

    def total_despesas_por_categoria(self):
        totais = {}

        for lancamento in self.lancamentos:
            if isinstance(lancamento, Despesa):
                nome = lancamento.categoria.nome
                totais[nome] = totais.get(nome, 0) + lancamento.valor

        return totais

    def despesas_por_forma_pagamento(self):
        totais = {}

        for lancamento in self.lancamentos:
            if isinstance(lancamento, Despesa):
                forma = lancamento.forma_pagamento
                totais[forma] = totais.get(forma, 0) + lancamento.valor

        return totais

    def percentual_por_categoria(self):
        totais = self.total_despesas_por_categoria()
        total_geral = sum(totais.values())

        if total_geral == 0:
            return {}

        return {
            categoria: round(valor / total_geral * 100, 2)
            for categoria, valor in totais.items()
        }

    def comparar_receitas_despesas(self):
        receitas = sum(
            lancamento.valor
            for lancamento in self.lancamentos
            if isinstance(lancamento, Receita)
        )

        despesas = sum(
            lancamento.valor
            for lancamento in self.lancamentos
            if isinstance(lancamento, Despesa)
        )

        return {
            "receitas": receitas,
            "despesas": despesas,
            "saldo": receitas - despesas,
        }

    def encontrar_mes_mais_economico(self):
        despesas_por_mes = {}

        for lancamento in self.lancamentos:
            if isinstance(lancamento, Despesa):
                chave = (lancamento.data.month, lancamento.data.year)

                despesas_por_mes[chave] = (
                    despesas_por_mes.get(chave, 0) + lancamento.valor
                )

        if not despesas_por_mes:
            return None

        mes, ano = min(
            despesas_por_mes,
            key=lambda chave: (
                despesas_por_mes[chave],
                chave[1],
                chave[0],
            ),
        )

        return {
            "mes": mes,
            "ano": ano,
            "total_despesas": despesas_por_mes[(mes, ano)],
        }

    def comparar_ultimos_meses(self, mes_referencia, ano_referencia):
        quantidade = self.configuracao["meses_comparacao"]

        if not isinstance(quantidade, int) or quantidade < 1:
            raise ValueError(
                "meses_comparacao deve ser um número inteiro positivo."
            )

        resultados = []

        for deslocamento in range(quantidade - 1, -1, -1):
            indice = ano_referencia * 12 + mes_referencia - 1
            indice -= deslocamento

            ano = indice // 12
            mes = indice % 12 + 1

            lancamentos_mes = [
                lancamento
                for lancamento in self.lancamentos
                if lancamento.data.month == mes
                and lancamento.data.year == ano
            ]

            receitas = sum(
                lancamento.valor
                for lancamento in lancamentos_mes
                if isinstance(lancamento, Receita)
            )

            despesas = sum(
                lancamento.valor
                for lancamento in lancamentos_mes
                if isinstance(lancamento, Despesa)
            )

            resultados.append({
                "mes": mes,
                "ano": ano,
                "receitas": receitas,
                "despesas": despesas,
                "saldo": receitas - despesas,
            })

        return resultados

    def avaliar_meta_economia(self):
        comparacao = self.comparar_receitas_despesas()

        receitas = comparacao["receitas"]
        saldo = comparacao["saldo"]
        meta = self.configuracao["meta_economia_percentual"]

        if receitas == 0:
            return {
                "meta": meta,
                "percentual_economia": None,
                "atingida": None,
            }

        percentual = round((saldo / receitas) * 100, 2)

        return {
            "meta": meta,
            "percentual_economia": percentual,
            "atingida": percentual >= meta,
        }

    def gerar(self):
        return {
            "despesas_por_categoria": self.total_despesas_por_categoria(),
            "despesas_por_pagamento": self.despesas_por_forma_pagamento(),
            "percentual_por_categoria": self.percentual_por_categoria(),
            "comparacao": self.comparar_receitas_despesas(),
        }