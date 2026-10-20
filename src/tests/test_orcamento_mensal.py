from datetime import date

import pytest

from entities.finance.categoria import Categoria
from entities.finance.orcamento_mensal import OrcamentoMensal
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa


def criar_lancamentos():
    categoria_receita = Categoria("Salário", "RECEITA")
    categoria_despesa = Categoria("Alimentação", "DESPESA", 500)

    receita = Receita(
        3000,
        categoria_receita,
        date(2026, 10, 5),
        "Salário",
        "PIX"
    )

    despesa = Despesa(
        200,
        categoria_despesa,
        date(2026, 10, 6),
        "Almoço",
        "DEBITO"
    )

    return receita, despesa


def test_adicionar_lancamento():
    receita, _ = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 3000)

    orcamento.adicionar_lancamento(receita)

    assert len(orcamento.lancamentos) == 1


def test_nao_adicionar_lancamento_de_outro_mes():
    receita, _ = criar_lancamentos()
    orcamento = OrcamentoMensal(9, 2026, 3000)

    with pytest.raises(ValueError):
        orcamento.adicionar_lancamento(receita)


def test_calcular_receitas():
    receita, _ = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 3000)
    orcamento.adicionar_lancamento(receita)

    assert orcamento.calcular_receitas() == 3000


def test_calcular_despesas():
    _, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 3000)
    orcamento.adicionar_lancamento(despesa)

    assert orcamento.calcular_despesas() == 200


def test_calcular_saldo():
    receita, despesa = criar_lancamentos()
    orcamento = OrcamentoMensal(10, 2026, 3000)

    orcamento.adicionar_lancamento(receita)
    orcamento.adicionar_lancamento(despesa)

    assert orcamento.calcular_saldo() == 2800