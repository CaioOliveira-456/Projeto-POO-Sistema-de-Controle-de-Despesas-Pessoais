from datetime import date

import pytest

from entities.transactions.lancamento import Lancamento


def test_criar_lancamento():
    lancamento = Lancamento(
        100.0,
        "Alimentacao",
        date(2026, 10, 6),
        "Almoço",
        "PIX"
    )

    assert lancamento.valor == 100.0
    assert lancamento.categoria == "Alimentacao"
    assert lancamento.data == date(2026, 10, 6)
    assert lancamento.descricao == "Almoço"
    assert lancamento.forma_pagamento == "PIX"


def test_valor_deve_ser_maior_que_zero():
    with pytest.raises(ValueError):
        Lancamento(
            0,
            "Alimentacao",
            date(2026, 10, 6),
            "Almoço",
            "PIX"
        )


def test_valor_deve_ser_numerico():
    with pytest.raises(TypeError):
        Lancamento(
            "100",
            "Alimentacao",
            date(2026, 10, 6),
            "Almoço",
            "PIX"
        )


def test_data_deve_ser_date():
    with pytest.raises(TypeError):
        Lancamento(
            100,
            "Alimentacao",
            "06/10/2026",
            "Almoço",
            "PIX"
        )


def test_forma_pagamento_invalida():
    with pytest.raises(ValueError):
        Lancamento(
            100,
            "Alimentacao",
            date(2026, 10, 6),
            "Almoço",
            "CHEQUE"
        )