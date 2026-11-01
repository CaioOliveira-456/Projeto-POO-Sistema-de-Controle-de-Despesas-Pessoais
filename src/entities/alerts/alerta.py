
from datetime import date


class Alerta:
    """Representa um alerta gerado a partir das regras financeiras."""

    def __init__(self, tipo, mensagem, data=None):
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data if data is not None else date.today()

    def emitir(self):
        """Retorna a mensagem do alerta."""
        return f"[{self.tipo}] {self.mensagem}"

    def __str__(self):
        return self.emitir()
