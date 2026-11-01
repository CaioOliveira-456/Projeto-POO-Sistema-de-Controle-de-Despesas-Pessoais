from uuid import uuid4


class Rastreavel:
    """Fornece identificação única aos objetos do sistema."""

    def __init__(self):
        self.id = str(uuid4())

    def obter_id(self):
        return self.id