class Categoria:
    """Representa uma categoria utilizada para organizar lançamentos financeiros."""

    def __init__(self, nome, tipo, limite_mensal=None, descricao=""):
        self.nome = nome
        self.tipo = tipo
        self.limite_mensal = limite_mensal
        self.descricao = descricao

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        if not isinstance(nome, str):
            raise TypeError("O nome deve ser uma string.")

        if not nome.strip():
            raise ValueError("O nome não pode ser vazio.")

        self._nome = nome.strip()

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        tipos_validos = ["RECEITA", "DESPESA"]

        if not isinstance(tipo, str):
            raise TypeError("O tipo deve ser uma string.")

        tipo = tipo.upper()

        if tipo not in tipos_validos:
            raise ValueError(
                "O tipo deve ser RECEITA ou DESPESA."
            )

        self._tipo = tipo

    @property
    def limite_mensal(self):
        return self._limite_mensal

    @limite_mensal.setter
    def limite_mensal(self, limite):
        if limite is not None:
            if not isinstance(limite, (int, float)):
                raise TypeError(
                    "O limite mensal deve ser numérico."
                )

            if limite < 0:
                raise ValueError(
                    "O limite mensal não pode ser negativo."
                )

        self._limite_mensal = (
            None if limite is None else float(limite)
        )

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        if not isinstance(descricao, str):
            raise TypeError(
                "A descrição deve ser uma string."
            )

        self._descricao = descricao.strip()

    def editar(self, nome=None, limite_mensal=None, descricao=None):
        """Permite alterar os dados da categoria."""

        if nome is not None:
            self.nome = nome

        if limite_mensal is not None:
            self.limite_mensal = limite_mensal

        if descricao is not None:
            self.descricao = descricao

    def validar(self):
        """Verifica se os dados da categoria são válidos."""

        if self.tipo == "RECEITA" and self.limite_mensal is not None:
            raise ValueError(
                "Categorias de receita não podem possuir limite mensal."
            )

        return True

    def __str__(self):
        return f"{self.nome} ({self.tipo})" 