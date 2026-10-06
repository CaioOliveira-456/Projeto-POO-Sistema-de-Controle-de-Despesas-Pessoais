from entities.transactions.lancamento import Lancamento


class Receita(Lancamento):
    """Representa uma receita financeira do sistema."""

    def calcular_impacto(self):
        return self.valor