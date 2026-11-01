from datetime import date

from entities.finance.categoria import Categoria
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa
from entities.transactions.lancamento import Lancamento
from entities.transactions.rastreavel import Rastreavel


def test_receita_herda_de_lancamento_e_rastreavel():
    categoria = Categoria("Salário", "RECEITA")

    receita = Receita(
        3000,
        categoria,
        date(2026, 11, 1),
        "Salário mensal",
        "PIX",
    )

    assert isinstance(receita, Lancamento)
    assert isinstance(receita, Rastreavel)


def test_despesa_herda_de_lancamento_e_rastreavel():
    categoria = Categoria("Alimentação", "DESPESA", 800)

    despesa = Despesa(
        200,
        categoria,
        date(2026, 11, 1),
        "Mercado",
        "PIX",
    )

    assert isinstance(despesa, Lancamento)
    assert isinstance(despesa, Rastreavel)


def test_lancamentos_possuem_ids_diferentes():
    categoria = Categoria("Salário", "RECEITA")

    receita1 = Receita(
        3000, categoria, date(2026, 11, 1), "Salário", "PIX"
    )

    receita2 = Receita(
        3000, categoria, date(2026, 11, 1), "Salário", "PIX"
    )

    assert receita1.obter_id() != receita2.obter_id()
def test_lancamento_herda_de_rastreavel_e_exportavel():
    from entities.transactions.exportavel import Exportavel

    categoria = Categoria("Salário", "RECEITA")
    receita = Receita(
        3000, categoria, date(2026, 11, 1), "Salário", "PIX"
    )

    assert isinstance(receita, Rastreavel)
    assert isinstance(receita, Exportavel)


def test_lancamento_pode_ser_convertido_em_dicionario():
    categoria = Categoria("Salário", "RECEITA")
    receita = Receita(
        3000, categoria, date(2026, 11, 1), "Salário", "PIX"
    )

    dados = receita.para_dict()

    assert dados["valor"] == 3000.0
    assert dados["descricao"] == "Salário"
    assert dados["forma_pagamento"] == "PIX"
    assert "id" in dados