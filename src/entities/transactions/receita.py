from entities.transactions.lancamento import Lancamento


class Receita(Lancamento):
    """Representa uma receita financeira do sistema."""

    TIPO_CATEGORIA = "RECEITA"

    def calcular_impacto(self):
        return self.valor