from datetime import date

from entities.finance.categoria import Categoria
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa
from entities.reports.relatorio import Relatorio


def test_encontrar_mes_mais_economico():
    categoria = Categoria("Alimentação", "DESPESA", 1000)

    lancamentos = [
        Despesa(400, categoria, date(2026, 1, 10), "Compra", "PIX"),
        Despesa(100, categoria, date(2026, 2, 10), "Compra", "PIX"),
        Despesa(200, categoria, date(2026, 2, 15), "Mercado", "PIX"),
        Despesa(500, categoria, date(2026, 3, 10), "Compra", "PIX"),
    ]

    resultado = Relatorio(lancamentos).encontrar_mes_mais_economico()

    assert resultado["mes"] == 2
    assert resultado["ano"] == 2026
    assert resultado["total_despesas"] == 300


def test_mes_mais_economico_sem_despesas():
    categoria = Categoria("Salário", "RECEITA")

    lancamentos = [
        Receita(2000, categoria, date(2026, 1, 5), "Salário", "PIX")
    ]

    resultado = Relatorio(lancamentos).encontrar_mes_mais_economico()

    assert resultado is None


def test_comparar_ultimos_meses():
    categoria_receita = Categoria("Salário", "RECEITA")
    categoria_despesa = Categoria("Alimentação", "DESPESA", 1000)

    lancamentos = [
        Receita(2000, categoria_receita, date(2026, 1, 5), "Salário", "PIX"),
        Despesa(500, categoria_despesa, date(2026, 1, 10), "Mercado", "PIX"),
        Receita(2500, categoria_receita, date(2026, 2, 5), "Salário", "PIX"),
        Despesa(700, categoria_despesa, date(2026, 2, 10), "Mercado", "PIX"),
        Receita(3000, categoria_receita, date(2026, 3, 5), "Salário", "PIX"),
        Despesa(800, categoria_despesa, date(2026, 3, 10), "Mercado", "PIX"),
    ]

    resultado = Relatorio(lancamentos).comparar_ultimos_meses(3, 2026)

    assert len(resultado) == 3
    assert resultado[0]["mes"] == 1
    assert resultado[1]["mes"] == 2
    assert resultado[2]["mes"] == 3
    assert resultado[2]["saldo"] == 2200


def test_comparar_ultimos_meses_entre_anos():
    relatorio = Relatorio([])

    resultado = relatorio.comparar_ultimos_meses(1, 2026)

    assert len(resultado) == 3
    assert resultado[0]["mes"] == 11
    assert resultado[0]["ano"] == 2025
    assert resultado[1]["mes"] == 12
    assert resultado[1]["ano"] == 2025
    assert resultado[2]["mes"] == 1
    assert resultado[2]["ano"] == 2026


def test_meta_economia_atingida():
    categoria_receita = Categoria("Salário", "RECEITA")
    categoria_despesa = Categoria("Contas", "DESPESA", 1000)

    lancamentos = [
        Receita(2000, categoria_receita, date(2026, 3, 5), "Salário", "PIX"),
        Despesa(1500, categoria_despesa, date(2026, 3, 10), "Contas", "PIX"),
    ]

    resultado = Relatorio(lancamentos).avaliar_meta_economia()

    assert resultado["percentual_economia"] == 25.0
    assert resultado["atingida"] is True


def test_meta_economia_nao_atingida():
    categoria_receita = Categoria("Salário", "RECEITA")
    categoria_despesa = Categoria("Contas", "DESPESA", 1000)

    lancamentos = [
        Receita(2000, categoria_receita, date(2026, 3, 5), "Salário", "PIX"),
        Despesa(1800, categoria_despesa, date(2026, 3, 10), "Contas", "PIX"),
    ]

    resultado = Relatorio(lancamentos).avaliar_meta_economia()

    assert resultado["percentual_economia"] == 10.0
    assert resultado["atingida"] is False


def test_meta_economia_sem_receitas():
    resultado = Relatorio([]).avaliar_meta_economia()

    assert resultado["percentual_economia"] is None
    assert resultado["atingida"] is None