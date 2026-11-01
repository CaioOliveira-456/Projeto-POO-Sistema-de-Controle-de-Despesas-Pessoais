
from datetime import date

from entities.alerts.alerta import Alerta
from entities.alerts.gerenciador_alertas import GerenciadorAlertas
from entities.finance.categoria import Categoria
from entities.finance.orcamento_mensal import OrcamentoMensal
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa


def criar_despesa(valor, limite=500):
    categoria = Categoria("Alimentação", "DESPESA", limite)

    return Despesa(
        valor,
        categoria,
        date(2026, 11, 1),
        "Compra",
        "PIX"
    )


def test_registrar_alerta():
    gerenciador = GerenciadorAlertas()
    alerta = Alerta("TESTE", "Mensagem de teste")

    gerenciador.registrar(alerta)

    assert len(gerenciador.alertas) == 1


def test_alerta_alto_valor():
    gerenciador = GerenciadorAlertas()

    alerta = gerenciador.verificar_alto_valor(criar_despesa(600))

    assert alerta is not None
    assert alerta.tipo == "ALTO VALOR"


def test_nao_gerar_alerta_alto_valor():
    gerenciador = GerenciadorAlertas()

    alerta = gerenciador.verificar_alto_valor(criar_despesa(400))

    assert alerta is None
    assert len(gerenciador.alertas) == 0


def test_alerta_limite_excedido():
    gerenciador = GerenciadorAlertas()

    alerta = gerenciador.verificar_limite(criar_despesa(600))

    assert alerta is not None
    assert alerta.tipo == "LIMITE EXCEDIDO"


def test_alerta_deficit_orcamentario():
    gerenciador = GerenciadorAlertas()
    categoria = Categoria("Alimentação", "DESPESA", 500)

    despesa = Despesa(
        600, categoria, date(2026, 11, 1), "Compra", "PIX"
    )

    orcamento = OrcamentoMensal(11, 2026, 1000)
    orcamento.adicionar_lancamento(despesa)

    alerta = gerenciador.verificar_deficit(orcamento)

    assert alerta is not None
    assert alerta.tipo == "DÉFICIT ORÇAMENTÁRIO"


def test_nao_gerar_alerta_deficit():
    gerenciador = GerenciadorAlertas()
    categoria = Categoria("Salário", "RECEITA")

    receita = Receita(
        3000, categoria, date(2026, 11, 1), "Salário", "PIX"
    )

    orcamento = OrcamentoMensal(11, 2026, 3000)
    orcamento.adicionar_lancamento(receita)

    alerta = gerenciador.verificar_deficit(orcamento)

    assert alerta is None


def test_alerta_soma_despesas_categoria():
    categoria = Categoria("Alimentação", "DESPESA", 500)
    orcamento = OrcamentoMensal(11, 2026, 2000)

    despesa1 = Despesa(
        300, categoria, date(2026, 11, 1), "Compra 1", "PIX"
    )
    despesa2 = Despesa(
        300, categoria, date(2026, 11, 2), "Compra 2", "PIX"
    )

    orcamento.adicionar_lancamento(despesa1)
    orcamento.adicionar_lancamento(despesa2)

    alertas = orcamento.gerenciador_alertas.alertas

    assert any(
        alerta.tipo == "LIMITE EXCEDIDO"
        for alerta in alertas
    )

