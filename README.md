# Projeto-POO-Sistema-de-Controle-de-Despesas-Pessoais

Projeto inicial em Python da disciplina Programação Orientada a Objetos do curso de Engenharia de Software.

O sistema terá como principal função o controle de movimentações com o intuito de gerenciar receitas, despesas e orçamentos pessoais. O sistema contará com relatórios automáticos e alertas de gastos, além de permitir o cadastro de categorias, o controle mensal das finanças e o cálculo de saldo disponível com o armazenamento persistente em JSON.

O foco do projeto é aplicar encapsulamento, herança, métodos especiais, validações rigorosas e relações entre múltiplas classes.

## Objetivo

Desenvolver um sistema de controle financeiro pessoal capaz de registrar receitas e despesas, organizar movimentações por categorias, controlar o orçamento mensal e apresentar informações sobre a situação financeira do usuário.

## Estrutura planejada

O projeto será desenvolvido em Python utilizando uma interface de linha de comando (CLI) e será organizado em módulos para separar as responsabilidades do sistema.

```text
Projeto-POO-Sistema-de-Controle-de-Despesas-Pessoais/
│
├── entidades/
│   ├── __init__.py
│   ├── lancamento.py
│   ├── receita.py
│   ├── despesa.py
│   ├── categoria.py
│   ├── orcamento_mensal.py
│   └── alerta.py
│
├── persistencia/
│   ├── __init__.py
│   └── json_repository.py
│
├── servicos/
│   ├── __init__.py
│   ├── alertas.py
│   └── relatorios.py
│
├── testes/
│   ├── __init__.py
│   └── ...
│
├── dados/
│   └── ...
│
├── main.py
├── settings.json
├── README.md
└── requirements.txt
```

### Classes planejadas

* **Lancamento:** classe base para representar movimentações financeiras.
* **Receita:** representa entradas financeiras e herda de `Lancamento`.
* **Despesa:** representa saídas financeiras e herda de `Lancamento`.
* **Categoria:** representa as categorias utilizadas para organizar receitas e despesas.
* **OrcamentoMensal:** responsável pelo controle dos lançamentos e orçamento de cada mês.
* **Alerta:** representa os alertas gerados pelo sistema.
