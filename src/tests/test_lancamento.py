
from datetime import date
import pytest

from entities.transactions.lancamento import Lancamento
from entities.finance.categoria import Categoria


def test_criar_lancamento():
    categoria = Categoria("Alimentação", "DESPESA")

    lancamento = Lancamento(
        100.0,
        categoria,
        date(2026, 10, 6),
        "Almoço",
        "PIX"
    )

    assert lancamento.valor == 100.0
    assert lancamento.categoria == categoria
    assert lancamento.descricao == "Almoço"


def test_valor_deve_ser_positivo():
    categoria = Categoria("Alimentação", "DESPESA")

    with pytest.raises(ValueError):
        Lancamento(
            -100,
            categoria,
            date(2026, 10, 6),
            "Almoço",
            "PIX"
        )


def test_valor_deve_ser_numerico():
    categoria = Categoria("Alimentação", "DESPESA")

    with pytest.raises(TypeError):
        Lancamento(
            "cem",
            categoria,
            date(2026, 10, 6),
            "Almoço",
            "PIX"
        )


def test_data_deve_ser_date():
    categoria = Categoria("Alimentação", "DESPESA")

    with pytest.raises(TypeError):
        Lancamento(
            100,
            categoria,
            "06/10/2026",
            "Almoço",
            "PIX"
        )


def test_forma_pagamento_invalida():
    categoria = Categoria("Alimentação", "DESPESA")

    with pytest.raises(ValueError):
        Lancamento(
            100,
            categoria,
            date(2026, 10, 6),
            "Almoço",
            "CHEQUE"
        )
