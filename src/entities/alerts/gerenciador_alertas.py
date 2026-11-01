
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


    def verificar_limite(self, despesa, lancamentos=None):
        """Verifica o total gasto na categoria durante o mês."""
        from entities.transactions.despesa import Despesa

        if despesa.categoria.limite_mensal is None:
            return None

        if lancamentos is None:
            lancamentos = [despesa]

        total_categoria = sum(
            lancamento.valor
            for lancamento in lancamentos
            if isinstance(lancamento, Despesa)
            and lancamento.categoria == despesa.categoria
        )

        limite = despesa.categoria.limite_mensal

        if total_categoria > limite:
            mensagem = (
                f"A categoria {despesa.categoria.nome} "
                f"ultrapassou seu limite mensal. "
                f"Total: R$ {total_categoria:.2f}; "
                f"limite: R$ {limite:.2f}."
            )

            # Evita registrar repetidamente o mesmo alerta.
            if any(
                alerta.tipo == "LIMITE EXCEDIDO"
                and alerta.mensagem == mensagem
                for alerta in self.alertas
            ):
                return None

            alerta = Alerta("LIMITE EXCEDIDO", mensagem)
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
