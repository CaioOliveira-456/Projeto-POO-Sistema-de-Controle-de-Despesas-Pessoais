
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa


class Relatorio:
    """Gera relatórios a partir dos lançamentos financeiros."""

    def __init__(self, lancamentos):
        self.lancamentos = lancamentos

    def total_despesas_por_categoria(self):
        """Retorna o total de despesas agrupadas por categoria."""
        totais = {}

        for lancamento in self.lancamentos:
            if isinstance(lancamento, Despesa):
                nome = lancamento.categoria.nome
                totais[nome] = totais.get(nome, 0) + lancamento.valor

        return totais

    def despesas_por_forma_pagamento(self):
        """Retorna o total de despesas por forma de pagamento."""
        totais = {}

        for lancamento in self.lancamentos:
            if isinstance(lancamento, Despesa):
                forma = lancamento.forma_pagamento
                totais[forma] = totais.get(forma, 0) + lancamento.valor

        return totais

    def percentual_por_categoria(self):
        """Calcula o percentual das despesas de cada categoria."""
        totais = self.total_despesas_por_categoria()
        total_geral = sum(totais.values())

        if total_geral == 0:
            return {}

        return {
            categoria: round(valor / total_geral * 100, 2)
            for categoria, valor in totais.items()
        }

    def comparar_receitas_despesas(self):
        """Compara o total de receitas e despesas."""
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

    def gerar(self):
        """Retorna os principais resultados financeiros."""
        return {
            "despesas_por_categoria": self.total_despesas_por_categoria(),
            "despesas_por_pagamento": self.despesas_por_forma_pagamento(),
            "percentual_por_categoria": self.percentual_por_categoria(),
            "comparacao": self.comparar_receitas_despesas(),
        }
