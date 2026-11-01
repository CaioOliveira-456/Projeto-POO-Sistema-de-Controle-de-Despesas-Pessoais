
from uuid import uuid4


class Rastreavel:
    """Fornece identificação única aos objetos do sistema."""

    def __init__(self, id=None):
        if id is not None and not isinstance(id, str):
            raise TypeError("O ID deve ser uma string.")

        if id == "":
            raise ValueError("O ID não pode ser vazio.")

        self.id = id if id is not None else str(uuid4())

    def obter_id(self):
        return self.id
