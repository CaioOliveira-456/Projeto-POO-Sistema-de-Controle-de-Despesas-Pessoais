from datetime import date

from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa
from entities.finance.categoria import Categoria


def test_receita_herda_de_lancamento():
    categoria = Categoria("Salário", "RECEITA")

    receita = Receita(
        3000,
        categoria,
        date(2026, 10, 6),
        "Salário",
        "PIX"
    )

    assert isinstance(receita, Receita)
    assert receita.valor == 3000.0
    assert receita.calcular_impacto() == 3000.0


def test_despesa_herda_de_lancamento():
    categoria = Categoria("Alimentação", "DESPESA", 500)

    despesa = Despesa(
        200,
        categoria,
        date(2026, 10, 6),
        "Almoço",
        "PIX"
    )

    assert isinstance(despesa, Despesa)
    assert despesa.valor == 200.0
    assert despesa.calcular_impacto() == -200.0


def test_despesa_verifica_limite():
    categoria = Categoria("Alimentação", "DESPESA", 500)

    despesa = Despesa(
        600,
        categoria,
        date(2026, 10, 6),
        "Compra do mês",
        "DEBITO"
    )

    assert despesa.verificar_limite() is True


def test_despesa_nao_excede_limite():
    categoria = Categoria("Alimentação", "DESPESA", 500)

    despesa = Despesa(
        300,
        categoria,
        date(2026, 10, 6),
        "Almoço",
        "PIX"
    )

    assert despesa.verificar_limite() is False