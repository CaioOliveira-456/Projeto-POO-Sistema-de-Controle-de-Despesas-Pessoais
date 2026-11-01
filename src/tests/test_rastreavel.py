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