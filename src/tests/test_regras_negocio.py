
import pytest
from datetime import date

from entities.finance.categoria import Categoria
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa


def test_receita_exige_categoria_receita():
    categoria = Categoria("Alimentação", "DESPESA", 500)

    with pytest.raises(ValueError):
        Receita(3000, categoria, date(2026, 11, 1), "Salário", "PIX")


def test_despesa_exige_categoria_despesa():
    categoria = Categoria("Salário", "RECEITA")

    with pytest.raises(ValueError):
        Despesa(200, categoria, date(2026, 11, 1), "Almoço", "PIX")


def test_categoria_receita_nao_aceita_limite():
    with pytest.raises(ValueError):
        Categoria("Salário", "RECEITA", 1000)


def test_lancamento_exige_objeto_categoria():
    with pytest.raises(TypeError):
        Receita(3000, "Salário", date(2026, 11, 1), "Salário", "PIX")
