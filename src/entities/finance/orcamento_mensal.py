class OrcamentoMensal:
    """Representa o orçamento financeiro de um determinado mês."""

    def __init__(self, mes, ano, orcamento_total):
        self.mes = mes
        self.ano = ano
        self.orcamento_total = orcamento_total
        self.lancamentos = []

    def adicionar_lancamento(self, lancamento):
        """Adiciona um lançamento ao orçamento do mês."""

        if lancamento.data.month != self.mes:
            raise ValueError(
                "O lançamento não pertence ao mês do orçamento."
            )

        if lancamento.data.year != self.ano:
            raise ValueError(
                "O lançamento não pertence ao ano do orçamento."
            )

        self.lancamentos.append(lancamento)

    def calcular_receitas(self):
        """Retorna o total de receitas do mês."""
        from entities.transactions.receita import Receita

        return sum(
            lancamento.valor
            for lancamento in self.lancamentos
            if isinstance(lancamento, Receita)
        )

    def calcular_despesas(self):
        """Retorna o total de despesas do mês."""
        from entities.transactions.despesa import Despesa

        return sum(
            lancamento.valor
            for lancamento in self.lancamentos
            if isinstance(lancamento, Despesa)
        )

    def calcular_saldo(self):
        """Calcula o saldo disponível do mês."""
        return self.calcular_receitas() - self.calcular_despesas()