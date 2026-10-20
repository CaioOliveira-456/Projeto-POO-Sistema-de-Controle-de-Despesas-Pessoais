
from datetime import date

from persistence.json_repository import (
    salvar_categorias,
    carregar_categorias,
    salvar_lancamentos,
    carregar_lancamentos,
)
from entities.finance.categoria import Categoria
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa


def test_persistir_objeto_categoria():
    categoria = Categoria("Alimentação", "DESPESA", 500)

    salvar_categorias([categoria])
    resultado = carregar_categorias()

    assert len(resultado) == 1
    assert isinstance(resultado[0], Categoria)
    assert resultado[0].nome == "Alimentação"
    assert resultado[0].limite_mensal == 500.0


def test_persistir_receita():
    categoria = Categoria("Salário", "RECEITA")
    receita = Receita(
        3000, categoria, date(2026, 10, 5), "Salário", "PIX"
    )

    salvar_lancamentos([receita])
    resultado = carregar_lancamentos()

    assert len(resultado) == 1
    assert isinstance(resultado[0], Receita)
    assert resultado[0].valor == 3000.0
    assert resultado[0].data == date(2026, 10, 5)


def test_persistir_despesa():
    categoria = Categoria("Alimentação", "DESPESA", 500)
    despesa = Despesa(
        200, categoria, date(2026, 10, 6), "Almoço", "DEBITO"
    )

    salvar_lancamentos([despesa])
    resultado = carregar_lancamentos()

    assert len(resultado) == 1
    assert isinstance(resultado[0], Despesa)
    assert resultado[0].valor == 200.0
    assert resultado[0].categoria.nome == "Alimentação"
