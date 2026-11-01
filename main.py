import argparse
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

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
    for categoria in categorias:
        if (
            categoria.nome.lower() == nome.lower()
            and categoria.tipo == tipo
        ):
            return categoria

    raise ValueError(
        f"Categoria '{nome}' do tipo {tipo} não encontrada. "
        "Cadastre-a primeiro."
    )


def adicionar_categoria(args):
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

    orcamento.lancamentos = [
        item for item in lancamentos
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
    lancamentos = carregar_lancamentos()

    orcamento = OrcamentoMensal(args.mes, args.ano, 0)

    orcamento.lancamentos = [
        lancamento for lancamento in lancamentos
        if lancamento.data.month == args.mes
        and lancamento.data.year == args.ano
    ]

    print(f"\nSaldo de {args.mes:02d}/{args.ano}")
    print(f"Receitas: R$ {orcamento.calcular_receitas():.2f}")
    print(f"Despesas: R$ {orcamento.calcular_despesas():.2f}")
    print(f"Saldo: R$ {orcamento.calcular_saldo():.2f}")


def gerar_relatorio(args):
    lancamentos = carregar_lancamentos()

    lancamentos_mes = [
        lancamento for lancamento in lancamentos
        if lancamento.data.month == args.mes
        and lancamento.data.year == args.ano
    ]

    relatorio = Relatorio(lancamentos_mes)
    historico = Relatorio(lancamentos)

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

    print("\nComparação financeira do mês:")
    print(f"  Receitas: R$ {comparacao['receitas']:.2f}")
    print(f"  Despesas: R$ {comparacao['despesas']:.2f}")
    print(f"  Saldo: R$ {comparacao['saldo']:.2f}")

    print("\nMês mais econômico do histórico:")

    mes_economico = historico.encontrar_mes_mais_economico()

    if mes_economico:
        print(
            f"  {mes_economico['mes']:02d}/{mes_economico['ano']} "
            f"- Despesas: R$ {mes_economico['total_despesas']:.2f}"
        )
    else:
        print("  Nenhuma despesa registrada.")

    print(
        f"\nComparação dos últimos meses "
        f"(referência: {args.mes:02d}/{args.ano}):"
    )

    comparacoes = historico.comparar_ultimos_meses(
        args.mes,
        args.ano,
    )

    for item in comparacoes:
        print(f"\n  {item['mes']:02d}/{item['ano']}")
        print(f"    Receitas: R$ {item['receitas']:.2f}")
        print(f"    Despesas: R$ {item['despesas']:.2f}")
        print(f"    Saldo: R$ {item['saldo']:.2f}")

    meta = relatorio.avaliar_meta_economia()

    print("\nMeta de economia:")

    if meta["percentual_economia"] is None:
        print("  Não foi possível calcular: nenhuma receita registrada.")
    else:
        print(f"  Meta definida: {meta['meta']}%")
        print(f"  Economia alcançada: {meta['percentual_economia']:.2f}%")

        if meta["atingida"]:
            print("  Meta de economia atingida!")
        else:
            print("  Meta de economia não atingida.")


def visualizar_alertas(args):
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
    parser = argparse.ArgumentParser(
        description="Sistema de Controle de Despesas Pessoais"
    )

    comandos = parser.add_subparsers(
        dest="comando",
        required=True,
    )

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

    parser_adicionar_categoria.add_argument("--nome", required=True)
    parser_adicionar_categoria.add_argument(
        "--tipo",
        required=True,
        choices=["RECEITA", "DESPESA"],
    )
    parser_adicionar_categoria.add_argument("--limite", type=float)
    parser_adicionar_categoria.add_argument("--descricao", default="")
    parser_adicionar_categoria.set_defaults(func=adicionar_categoria)

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

        parser_adicionar.add_argument("--valor", type=float, required=True)
        parser_adicionar.add_argument("--categoria", required=True)
        parser_adicionar.add_argument("--descricao", required=True)
        parser_adicionar.add_argument(
            "--pagamento",
            required=True,
            choices=["DINHEIRO", "DEBITO", "CREDITO", "PIX"],
        )
        parser_adicionar.add_argument("--data")
        parser_adicionar.set_defaults(func=funcao)

    parser_saldo = comandos.add_parser(
        "saldo",
        help="Consultar saldo mensal",
    )

    parser_saldo.add_argument(
        "--mes",
        type=int,
        default=date.today().month,
        choices=range(1, 13),
    )
    parser_saldo.add_argument(
        "--ano",
        type=int,
        default=date.today().year,
    )
    parser_saldo.set_defaults(func=consultar_saldo)

    parser_relatorio = comandos.add_parser(
        "relatorio",
        help="Gerar relatórios financeiros",
    )

    parser_relatorio.add_argument(
        "--mes",
        type=int,
        default=date.today().month,
        choices=range(1, 13),
    )
    parser_relatorio.add_argument(
        "--ano",
        type=int,
        default=date.today().year,
    )
    parser_relatorio.set_defaults(func=gerar_relatorio)

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