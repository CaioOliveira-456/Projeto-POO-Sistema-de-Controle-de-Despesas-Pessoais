from src.entities.reports.relatorio import Relatorio
from src.services.comparador_financeiro import ComparadorFinanceiroMixin

class RelatorioMensal(Relatorio, ComparadorFinanceiroMixin):
    """Representa o relatório comparativo das movimentações financeiras mensais."""
    pass