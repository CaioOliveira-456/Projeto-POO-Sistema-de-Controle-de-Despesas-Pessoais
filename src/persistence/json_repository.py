
import json
from datetime import date
from pathlib import Path

from entities.finance.categoria import Categoria
from entities.transactions.receita import Receita
from entities.transactions.despesa import Despesa


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def salvar_dados(nome_arquivo, dados):
    caminho = DATA_DIR / nome_arquivo

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_dados(nome_arquivo):
    caminho = DATA_DIR / nome_arquivo

    if not caminho.exists():
        return []

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_categorias(categorias):
    dados = [
        {
            "nome": categoria.nome,
            "tipo": categoria.tipo,
            "limite_mensal": categoria.limite_mensal,
            "descricao": categoria.descricao,
        }
        for categoria in categorias
    ]

    salvar_dados("categorias.json", dados)


def carregar_categorias():
    dados = carregar_dados("categorias.json")

    return [
        Categoria(
            item["nome"],
            item["tipo"],
            item.get("limite_mensal"),
            item.get("descricao", ""),
        )
        for item in dados
    ]


def salvar_lancamentos(lancamentos):
    dados = [
        {
            "tipo": type(lancamento).__name__,
            "valor": lancamento.valor,
            "categoria": {
                "nome": lancamento.categoria.nome,
                "tipo": lancamento.categoria.tipo,
                "limite_mensal": lancamento.categoria.limite_mensal,
                "descricao": lancamento.categoria.descricao,
            },
            "data": lancamento.data.isoformat(),
            "descricao": lancamento.descricao,
            "forma_pagamento": lancamento.forma_pagamento,
        }
        for lancamento in lancamentos
    ]

    salvar_dados("lancamentos.json", dados)


def carregar_lancamentos():
    dados = carregar_dados("lancamentos.json")
    lancamentos = []

    for item in dados:
        dados_categoria = item["categoria"]

        categoria = Categoria(
            dados_categoria["nome"],
            dados_categoria["tipo"],
            dados_categoria.get("limite_mensal"),
            dados_categoria.get("descricao", ""),
        )

        data_lancamento = date.fromisoformat(item["data"])

        classe = {
            "Receita": Receita,
            "Despesa": Despesa,
        }.get(item["tipo"])

        if classe is None:
            raise ValueError(
                f"Tipo de lançamento desconhecido: {item['tipo']}"
            )

        lancamento = classe(
            item["valor"],
            categoria,
            data_lancamento,
            item["descricao"],
            item["forma_pagamento"],
        )

        lancamentos.append(lancamento)

    return lancamentos
