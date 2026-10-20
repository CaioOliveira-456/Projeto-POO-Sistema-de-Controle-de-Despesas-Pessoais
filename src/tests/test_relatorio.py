
from datetime import date

from entities.finance.categoria import Categoria
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa
from entities.reports.relatorio import Relatorio


def criar_relatorio():
    salario = Categoria("Salário", "RECEITA")
    alimentacao = Categoria("Alimentação", "DESPESA", 500)
    transporte = Categoria("Transporte", "DESPESA", 300)

    lancamentos = [
        Receita(3000, salario, date(2026, 10, 5), "Salário", "PIX"),
        Despesa(200, alimentacao, date(2026, 10, 6), "Mercado", "DEBITO"),
        Despesa(100, alimentacao, date(2026, 10, 7), "Almoço", "PIX"),
        Despesa(150, transporte, date(2026, 10, 8), "Combustível", "CREDITO"),
    ]

    return Relatorio(lancamentos)


def test_despesas_por_categoria():
    relatorio = criar_relatorio()

    assert relatorio.total_despesas_por_categoria() == {
        "Alimentação": 300,
        "Transporte": 150,
    }


def test_despesas_por_pagamento():
    relatorio = criar_relatorio()

    assert relatorio.despesas_por_forma_pagamento() == {
        "DEBITO": 200,
        "PIX": 100,
        "CREDITO": 150,
    }


def test_percentual_por_categoria():
    relatorio = criar_relatorio()

    assert relatorio.percentual_por_categoria() == {
        "Alimentação": 66.67,
        "Transporte": 33.33,
    }


def test_comparar_receitas_despesas():
    relatorio = criar_relatorio()

    assert relatorio.comparar_receitas_despesas() == {
        "receitas": 3000,
        "despesas": 450,
        "saldo": 2550,
    }


def test_gerar_relatorio_completo():
    relatorio = criar_relatorio()

    resultado = relatorio.gerar()

    assert "despesas_por_categoria" in resultado
    assert "despesas_por_pagamento" in resultado
    assert "percentual_por_categoria" in resultado
    assert "comparacao" in resultado
