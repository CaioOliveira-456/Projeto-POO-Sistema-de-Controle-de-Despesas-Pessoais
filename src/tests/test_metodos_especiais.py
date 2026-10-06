from datetime import date

from entities.transactions.lancamento import Lancamento
from entities.finance.categoria import Categoria


def criar_lancamento(valor=100):
    categoria = Categoria("Alimentação", "DESPESA")

    return Lancamento(
        valor,
        categoria,
        date(2026, 10, 6),
        "Almoço",
        "PIX"
    )


def test_str():
    lancamento = criar_lancamento()

    assert str(lancamento) == "06/10/2026 - Almoço: R$ 100.00"


def test_repr():
    lancamento = criar_lancamento()

    resultado = repr(lancamento)

    assert "Lancamento(" in resultado
    assert "valor=100" in resultado
    assert "descricao='Almoço'" in resultado


def test_eq():
    lancamento1 = criar_lancamento()
    lancamento2 = criar_lancamento()

    assert lancamento1 == lancamento2


def test_lt():
    lancamento1 = criar_lancamento()
    lancamento2 = Lancamento(
        200,
        lancamento1.categoria,
        date(2026, 10, 7),
        "Jantar",
        "PIX"
    )

    assert lancamento1 < lancamento2


def test_add():
    lancamento1 = criar_lancamento(100)
    lancamento2 = criar_lancamento(200)

    assert lancamento1 + lancamento2 == 300