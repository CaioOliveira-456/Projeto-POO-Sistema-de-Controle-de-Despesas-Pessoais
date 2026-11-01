
import json
from pathlib import Path


class ConfiguracaoRepository:
    """Responsável por carregar as configurações do sistema."""

    def __init__(self):
        self.caminho = (
            Path(__file__).resolve().parents[2] / "settings.json"
        )

    def carregar(self):
        """Carrega as configurações do arquivo JSON."""
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
