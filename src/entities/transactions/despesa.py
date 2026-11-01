from entities.transactions.lancamento import Lancamento
from entities.transactions.rastreavel import Rastreavel


class Despesa(Lancamento, Rastreavel):
    """Representa uma despesa financeira do sistema."""

    TIPO_CATEGORIA = "DESPESA"

    def calcular_impacto(self):
        return -self.valor

    def verificar_limite(self):
        if self.categoria.limite_mensal is None:
            return False

        return self.valor > self.categoria.limite_mensal