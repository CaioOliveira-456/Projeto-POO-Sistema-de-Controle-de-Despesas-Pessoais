from datetime import date


class Lancamento:
    """Representa uma movimentação financeira genérica do sistema."""

    def __init__(self, valor, categoria, data, descricao, forma_pagamento):
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao
        self.forma_pagamento = forma_pagamento

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        if not isinstance(valor, (int, float)):
            raise TypeError("O valor deve ser numérico.")

        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        self._valor = float(valor)

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, categoria):
        if categoria is None:
            raise ValueError("A categoria é obrigatória.")

        self._categoria = categoria

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if not isinstance(data, date):
            raise TypeError("A data deve ser um objeto date.")

        self._data = data

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        if not isinstance(descricao, str):
            raise TypeError("A descrição deve ser uma string.")

        self._descricao = descricao

    @property
    def forma_pagamento(self):
        return self._forma_pagamento

    @forma_pagamento.setter
    def forma_pagamento(self, forma_pagamento):
        formas_validas = ["DINHEIRO", "DEBITO", "CREDITO", "PIX"]

        if forma_pagamento.upper() not in formas_validas:
            raise ValueError(
                "Forma de pagamento inválida. "
                "Use DINHEIRO, DEBITO, CREDITO ou PIX."
            )

        self._forma_pagamento = forma_pagamento.upper()

    def __str__(self):
        return (
            f"{self.data.strftime('%d/%m/%Y')} - "
            f"{self.descricao}: R$ {self.valor:.2f}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"valor={self.valor!r}, "
            f"categoria={self.categoria!r}, "
            f"data={self.data!r}, "
            f"descricao={self.descricao!r}, "
            f"forma_pagamento={self.forma_pagamento!r})"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Lancamento):
            return NotImplemented

        return (
            self.data == outro.data
            and self.descricao == outro.descricao
        )

    def __lt__(self, outro):
        if not isinstance(outro, Lancamento):
            return NotImplemented

        return self.data < outro.data

    def __add__(self, outro):
        if not isinstance(outro, Lancamento):
            return NotImplemented

        if type(self) is not type(outro):
            raise TypeError(
                "Só é possível somar lançamentos do mesmo tipo."
            )

        return self.valor + outro.valor