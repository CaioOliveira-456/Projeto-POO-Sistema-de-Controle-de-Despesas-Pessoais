# Projeto-POO-Sistema-de-Controle-de-Despesas-Pessoais

Projeto inicial em Python da disciplina Programação Orientada a Objetos do curso de Engenharia de Software.

O sistema terá como principal função o controle de movimentações com o intuito de gerenciar receitas, despesas e orçamentos pessoais. O sistema contará com relatórios automáticos e alertas de gastos, além de permitir o cadastro de categorias, o controle mensal das finanças e o cálculo de saldo disponível com o armazenamento persistente em JSON.

O foco do projeto é aplicar encapsulamento, herança, métodos especiais, validações rigorosas e relações entre múltiplas classes.

## Objetivo

Desenvolver um sistema de controle financeiro pessoal capaz de registrar receitas e despesas, organizar movimentações por categorias, controlar o orçamento mensal e apresentar informações sobre a situação financeira do usuário.

## Estrutura planejada

O projeto será organizado em diferentes módulos para separar as responsabilidades do sistema.

```text
Projeto-POO-Sistema-de-Controle-de-Despesas-Pessoais/
│
├── general/
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── lancamento.py
│   │   ├── receita.py
│   │   ├── despesa.py
│   │   ├── categoria.py
│   │   ├── orcamento_mensal.py
│   │   └── alerta.py
│   │
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── json_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── alertas.py
│   │   └── relatorios.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   └── ...
│   │
│   └── data/
│       └── ...
│
├── main.py
├── settings.json
├── README.md
└── requirements.txt
```

### Classes planejadas

* **Lancamento** — classe base para representar movimentações financeiras.
* **Receita** — representa entradas financeiras.
* **Despesa** — representa saídas financeiras.
* **Categoria** — organiza as receitas e despesas.
* **OrcamentoMensal** — controla o orçamento e o saldo mensal.
* **Alerta** — representa notificações relacionadas às regras financeiras.

O sistema terá uma interface de linha de comando (CLI) para interação com o usuário.
