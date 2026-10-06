import pytest

from entities.finance.categoria import Categoria


def test_criar_categoria_despesa():
    categoria = Categoria(
        "Alimentação",
        "DESPESA",
        800,
        "Gastos com alimentação"
    )

    assert categoria.nome == "Alimentação"
    assert categoria.tipo == "DESPESA"
    assert categoria.limite_mensal == 800.0
    assert categoria.descricao == "Gastos com alimentação"


def test_tipo_deve_ser_receita_ou_despesa():
    with pytest.raises(ValueError):
        Categoria("Teste", "INVESTIMENTO")


def test_nome_nao_pode_ser_vazio():
    with pytest.raises(ValueError):
        Categoria("", "DESPESA")


def test_limite_nao_pode_ser_negativo():
    with pytest.raises(ValueError):
        Categoria("Alimentação", "DESPESA", -100)


def test_categoria_receita_nao_pode_ter_limite():
    categoria = Categoria("Salário", "RECEITA", 500)

    with pytest.raises(ValueError):
        categoria.validar()


def test_categoria_receita_sem_limite_e_valida():
    categoria = Categoria("Salário", "RECEITA")

    assert categoria.validar() is True