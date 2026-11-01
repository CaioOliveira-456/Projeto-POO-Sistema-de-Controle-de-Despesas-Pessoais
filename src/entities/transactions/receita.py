from entities.transactions.lancamento import Lancamento
from entities.transactions.rastreavel import Rastreavel


class Receita(Lancamento, Rastreavel):
    """Representa uma receita financeira do sistema."""

    TIPO_CATEGORIA = "RECEITA"

    def calcular_impacto(self):
        return self.valor