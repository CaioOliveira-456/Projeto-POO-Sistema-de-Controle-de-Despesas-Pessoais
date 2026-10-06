from entities.transactions.lancamento import Lancamento


class Despesa(Lancamento):
    """Representa uma despesa financeira do sistema."""

    def calcular_impacto(self):
        return -self.valor

    def verificar_limite(self):
        if self.categoria.limite_mensal is None:
            return False

        return self.valor > self.categoria.limite_mensal