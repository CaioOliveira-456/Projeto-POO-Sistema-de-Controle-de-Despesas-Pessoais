
import argparse
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# Permite importar os pacotes que estão dentro de src/
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from entities.finance.categoria import Categoria
from entities.finance.orcamento_mensal import OrcamentoMensal
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa
from entities.reports.relatorio import Relatorio
from entities.alerts.gerenciador_alertas import GerenciadorAlertas

from persistence.json_repository import (
    carregar_categorias,
    salvar_categorias,
    carregar_lancamentos,
    salvar_lancamentos,
)


def obter_categoria(nome, tipo, categorias):
    """Localiza uma categoria pelo nome e pelo tipo."""
    for categoria in categorias:
        if categoria.nome.lower() == nome.lower() and categoria.tipo == tipo:
            return categoria

    raise ValueError(
        f"Categoria '{nome}' do tipo {tipo} não encontrada. "
        "Cadastre-a primeiro."
    )


def adicionar_categoria(args):
    """Cadastra e salva uma categoria."""
    categorias = carregar_categorias()

    for categoria in categorias:
        if categoria.nome.lower() == args.nome.lower():
            if categoria.tipo == args.tipo:
                raise ValueError("Essa categoria já está cadastrada.")

    categoria = Categoria(
        args.nome,
        args.tipo,
        args.limite,
        args.descricao,
    )

    categorias.append(categoria)
    salvar_categorias(categorias)

    print(f"Categoria '{categoria.nome}' cadastrada com sucesso!")


def adicionar_lancamento(args, tipo):
    """Registra uma receita ou despesa e salva os dados."""
    categorias = carregar_categorias()
    lancamentos = carregar_lancamentos()

    categoria = obter_categoria(args.categoria, tipo, categorias)

    data_lancamento = (
        date.fromisoformat(args.data) if args.data else date.today()
    )

    classe = Receita if tipo == "RECEITA" else Despesa

    lancamento = classe(
        args.valor,
        categoria,
        data_lancamento,
        args.descricao,
        args.pagamento,
    )

    orcamento = OrcamentoMensal(
        data_lancamento.month,
        data_lancamento.year,
        0,
    )

    # Carrega os lançamentos anteriores daquele mesmo mês.
    orcamento.lancamentos = [
        item
        for item in lancamentos
        if item.data.month == data_lancamento.month
        and item.data.year == data_lancamento.year
    ]

    orcamento.adicionar_lancamento(lancamento)

    lancamentos.append(lancamento)
    salvar_lancamentos(lancamentos)

    print(
        f"{tipo.capitalize()} registrada com sucesso: "
        f"R$ {lancamento.valor:.2f}"
    )

    if orcamento.gerenciador_alertas.alertas:
        print("\nAlertas gerados:")

        for alerta in orcamento.gerenciador_alertas.alertas:
            print(alerta)


def adicionar_receita(args):
    adicionar_lancamento(args, "RECEITA")


def adicionar_despesa(args):
    adicionar_lancamento(args, "DESPESA")


def consultar_saldo(args):
    """Exibe o saldo de um mês específico."""
    lancamentos = carregar_lancamentos()

    orcamento = OrcamentoMensal(args.mes, args.ano, 0)

    orcamento.lancamentos = [
        lancamento
        for lancamento in lancamentos
        if lancamento.data.month == args.mes
        and lancamento.data.year == args.ano
    ]

    print(f"\nSaldo de {args.mes:02d}/{args.ano}")
    print(f"Receitas: R$ {orcamento.calcular_receitas():.2f}")
    print(f"Despesas: R$ {orcamento.calcular_despesas():.2f}")
    print(f"Saldo: R$ {orcamento.calcular_saldo():.2f}")


def gerar_relatorio(args):
    """Gera os relatórios financeiros de um mês."""
    lancamentos = carregar_lancamentos()

    lancamentos_mes = [
        lancamento
        for lancamento in lancamentos
        if lancamento.data.month == args.mes
        and lancamento.data.year == args.ano
    ]

    relatorio = Relatorio(lancamentos_mes)
    dados = relatorio.gerar()

    print(f"\nRelatórios de {args.mes:02d}/{args.ano}")

    print("\nDespesas por categoria:")
    if dados["despesas_por_categoria"]:
        for categoria, valor in dados["despesas_por_categoria"].items():
            print(f"  {categoria}: R$ {valor:.2f}")
    else:
        print("  Nenhuma despesa registrada.")

    print("\nDespesas por forma de pagamento:")
    if dados["despesas_por_pagamento"]:
        for forma, valor in dados["despesas_por_pagamento"].items():
            print(f"  {forma}: R$ {valor:.2f}")
    else:
        print("  Nenhuma despesa registrada.")

    print("\nPercentual por categoria:")
    if dados["percentual_por_categoria"]:
        for categoria, percentual in dados["percentual_por_categoria"].items():
            print(f"  {categoria}: {percentual:.2f}%")
    else:
        print("  Nenhum percentual disponível.")

    comparacao = dados["comparacao"]

    print("\nComparação financeira:")
    print(f"  Receitas: R$ {comparacao['receitas']:.2f}")
    print(f"  Despesas: R$ {comparacao['despesas']:.2f}")
    print(f"  Saldo: R$ {comparacao['saldo']:.2f}")


def visualizar_alertas(args):
    """Recalcula e exibe os alertas dos lançamentos salvos."""
    lancamentos = carregar_lancamentos()

    if not lancamentos:
        print("Não existem lançamentos registrados.")
        return

    lancamentos_por_mes = defaultdict(list)

    for lancamento in lancamentos:
        chave = (lancamento.data.month, lancamento.data.year)
        lancamentos_por_mes[chave].append(lancamento)

    todos_alertas = []

    for (mes, ano), itens in lancamentos_por_mes.items():
        orcamento = OrcamentoMensal(mes, ano, 0)
        orcamento.lancamentos = itens

        gerenciador = GerenciadorAlertas()

        for lancamento in itens:
            if isinstance(lancamento, Despesa):
                gerenciador.verificar_alto_valor(lancamento)
                gerenciador.verificar_limite(lancamento, itens)

        gerenciador.verificar_deficit(orcamento)
        todos_alertas.extend(gerenciador.alertas)

    if not todos_alertas:
        print("Nenhum alerta identificado.")
        return

    print("\nAlertas financeiros:")

    for alerta in todos_alertas:
        print(alerta)


def criar_parser():
    """Configura os comandos e argumentos da CLI."""
    parser = argparse.ArgumentParser(
        description="Sistema de Controle de Despesas Pessoais"
    )

    comandos = parser.add_subparsers(
        dest="comando",
        required=True,
    )

    # Comando: categoria adicionar
    parser_categoria = comandos.add_parser(
        "categoria",
        help="Gerenciar categorias",
    )

    sub_categoria = parser_categoria.add_subparsers(
        dest="acao",
        required=True,
    )

    parser_adicionar_categoria = sub_categoria.add_parser(
        "adicionar",
        help="Cadastrar uma categoria",
    )

    parser_adicionar_categoria.add_argument(
        "--nome",
        required=True,
        help="Nome da categoria",
    )

    parser_adicionar_categoria.add_argument(
        "--tipo",
        required=True,
        choices=["RECEITA", "DESPESA"],
        help="Tipo da categoria",
    )

    parser_adicionar_categoria.add_argument(
        "--limite",
        type=float,
        help="Limite mensal da categoria",
    )

    parser_adicionar_categoria.add_argument(
        "--descricao",
        default="",
        help="Descrição da categoria",
    )

    parser_adicionar_categoria.set_defaults(
        func=adicionar_categoria
    )

    # Comandos: receita adicionar e despesa adicionar
    for nome_comando, funcao, descricao in [
        ("receita", adicionar_receita, "Registrar uma receita"),
        ("despesa", adicionar_despesa, "Registrar uma despesa"),
    ]:
        parser_tipo = comandos.add_parser(
            nome_comando,
            help=descricao,
        )

        sub_tipo = parser_tipo.add_subparsers(
            dest="acao",
            required=True,
        )

        parser_adicionar = sub_tipo.add_parser(
            "adicionar",
            help=descricao,
        )

        parser_adicionar.add_argument(
            "--valor",
            type=float,
            required=True,
            help="Valor do lançamento",
        )

        parser_adicionar.add_argument(
            "--categoria",
            required=True,
            help="Nome da categoria",
        )

        parser_adicionar.add_argument(
            "--descricao",
            required=True,
            help="Descrição do lançamento",
        )

        parser_adicionar.add_argument(
            "--pagamento",
            required=True,
            choices=["DINHEIRO", "DEBITO", "CREDITO", "PIX"],
            help="Forma de pagamento",
        )

        parser_adicionar.add_argument(
            "--data",
            help="Data no formato AAAA-MM-DD (padrão: hoje)",
        )

        parser_adicionar.set_defaults(func=funcao)

    # Comando: saldo
    parser_saldo = comandos.add_parser(
        "saldo",
        help="Consultar saldo mensal",
    )

    parser_saldo.add_argument(
        "--mes",
        type=int,
        default=date.today().month,
        choices=range(1, 13),
        help="Mês consultado",
    )

    parser_saldo.add_argument(
        "--ano",
        type=int,
        default=date.today().year,
        help="Ano consultado",
    )

    parser_saldo.set_defaults(func=consultar_saldo)

    # Comando: relatorio
    parser_relatorio = comandos.add_parser(
        "relatorio",
        help="Gerar relatórios financeiros",
    )

    parser_relatorio.add_argument(
        "--mes",
        type=int,
        default=date.today().month,
        choices=range(1, 13),
        help="Mês do relatório",
    )

    parser_relatorio.add_argument(
        "--ano",
        type=int,
        default=date.today().year,
        help="Ano do relatório",
    )

    parser_relatorio.set_defaults(func=gerar_relatorio)

    # Comando: alertas
    parser_alertas = comandos.add_parser(
        "alertas",
        help="Visualizar alertas financeiros",
    )

    parser_alertas.set_defaults(func=visualizar_alertas)

    return parser


def main():
    parser = criar_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except (ValueError, TypeError, KeyError, OSError) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
