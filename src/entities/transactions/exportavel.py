class Exportavel:
    """Fornece métodos para converter objetos em dicionários."""

    def para_dict(self):
        """Converte os atributos públicos do objeto em um dicionário."""
        return {
            chave.lstrip("_"): valor
            for chave, valor in self.__dict__.items()
        }