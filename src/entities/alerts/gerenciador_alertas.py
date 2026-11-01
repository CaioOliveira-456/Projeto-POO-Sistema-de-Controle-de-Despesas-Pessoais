
from entities.alerts.alerta import Alerta


class GerenciadorAlertas:
    """Gerencia a criação, registro e verificação dos alertas financeiros."""

    def __init__(self):
        self.alertas = []

    def registrar(self, alerta):
        """Registra um alerta."""
        if not isinstance(alerta, Alerta):
            raise TypeError("É necessário registrar um objeto Alerta.")

        self.alertas.append(alerta)

    def verificar_alto_valor(self, despesa):
        """Verifica se uma despesa ultrapassa R$ 500."""
        if despesa.valor > 500:
            alerta = Alerta(
                "ALTO VALOR",
                f"Despesa de R$ {despesa.valor:.2f} identificada."
            )
            self.registrar(alerta)
            return alerta

        return None

    def verificar_limite(self, despesa):
        """Verifica se uma despesa ultrapassa o limite da categoria."""
        if despesa.verificar_limite():
            alerta = Alerta(
                "LIMITE EXCEDIDO",
                f"A categoria {despesa.categoria.nome} "
                f"ultrapassou seu limite mensal."
            )
            self.registrar(alerta)
            return alerta

        return None

    def verificar_deficit(self, orcamento):
        """Verifica se o saldo mensal está negativo."""
        saldo = orcamento.calcular_saldo()

        if saldo < 0:
            alerta = Alerta(
                "DÉFICIT ORÇAMENTÁRIO",
                f"O orçamento apresenta saldo negativo de R$ {abs(saldo):.2f}."
            )
            self.registrar(alerta)
            return alerta

        return None
