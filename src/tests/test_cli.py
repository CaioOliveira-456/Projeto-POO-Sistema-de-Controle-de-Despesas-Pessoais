
import pytest
import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PROJETO))

from main import criar_parser


def test_comando_categoria():
    parser = criar_parser()

    args = parser.parse_args([
        "categoria", "adicionar",
        "--nome", "Alimentação",
        "--tipo", "DESPESA",
        "--limite", "500",
    ])

    assert args.nome == "Alimentação"
    assert args.tipo == "DESPESA"
    assert args.limite == 500
    assert args.func.__name__ == "adicionar_categoria"


def test_comando_receita():
    parser = criar_parser()

    args = parser.parse_args([
        "receita", "adicionar",
        "--valor", "3000",
        "--categoria", "Salário",
        "--descricao", "Pagamento mensal",
        "--pagamento", "PIX",
    ])

    assert args.valor == 3000
    assert args.categoria == "Salário"
    assert args.func.__name__ == "adicionar_receita"


def test_comando_despesa():
    parser = criar_parser()

    args = parser.parse_args([
        "despesa", "adicionar",
        "--valor", "150",
        "--categoria", "Alimentação",
        "--descricao", "Supermercado",
        "--pagamento", "PIX",
    ])

    assert args.valor == 150
    assert args.categoria == "Alimentação"
    assert args.func.__name__ == "adicionar_despesa"


def test_comando_saldo():
    parser = criar_parser()

    args = parser.parse_args([
        "saldo",
        "--mes", "11",
        "--ano", "2026",
    ])

    assert args.mes == 11
    assert args.ano == 2026
    assert args.func.__name__ == "consultar_saldo"


def test_comando_relatorio():
    parser = criar_parser()

    args = parser.parse_args([
        "relatorio",
        "--mes", "11",
        "--ano", "2026",
    ])

    assert args.mes == 11
    assert args.ano == 2026
    assert args.func.__name__ == "gerar_relatorio"


def test_comando_alertas():
    parser = criar_parser()

    args = parser.parse_args(["alertas"])

    assert args.func.__name__ == "visualizar_alertas"


def test_comando_invalido():
    parser = criar_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["comando_inexistente"])
