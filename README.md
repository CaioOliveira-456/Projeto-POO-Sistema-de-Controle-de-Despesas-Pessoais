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
├── src/
│   │
│   ├── entities/
│   │   ├── __init__.py
│   │   │
│   │   ├── transactions/
│   │   │   ├── __init__.py
│   │   │   ├── lancamento.py
│   │   │   ├── receita.py
│   │   │   └── despesa.py
│   │   │
│   │   ├── finance/
│   │   │   ├── __init__.py
│   │   │   ├── categoria.py
│   │   │   └── orcamento_mensal.py
│   │   │
│   │   ├── alerts/
│   │   │   ├── __init__.py
│   │   │   ├── alerta.py
│   │   │   └── gerenciador_alertas.py
│   │   │
│   │   └── reports/
│   │       ├── __init__.py
│   │       └── relatorio.py
│   │
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── json_repository.py
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

#### Lançamentos

* **Lancamento** — classe base para representar movimentações financeiras.
* **Receita** — representa entradas financeiras.
* **Despesa** — representa saídas financeiras.

#### Controle financeiro

* **Categoria** — organiza as receitas e despesas por categorias.
* **OrcamentoMensal** — controla o orçamento, os lançamentos e o saldo mensal.

#### Alertas

* **Alerta** — representa notificações relacionadas às regras financeiras.
* **GerenciadorAlertas** — gerencia e verifica os alertas gerados pelo sistema.

#### Relatórios

* **Relatorio** — classe base para os relatórios financeiros.

O sistema terá uma interface de linha de comando (CLI) para interação com o usuário.


### Diagrama UML

```mermaid
    classDiagram

    class Lancamento {
        -float valor
        -Categoria categoria
        -date data
        -str descricao
        -str forma_pagamento
        +__str__()
        +__repr__()
        +__eq__()
        +__lt__()
        +__add__()
    }

    class Receita {
        +calcular_impacto()
    }

    class Despesa {
        +calcular_impacto()
        +verificar_limite()
    }

    class Categoria {
        -str nome
        -str tipo
        -float limite_mensal
        -str descricao
        +editar()
        +validar()
    }

    class OrcamentoMensal {
        -int mes
        -int ano
        -float orcamento_total
        -list lancamentos
        +adicionar_lancamento()
        +calcular_receitas()
        +calcular_despesas()
        +calcular_saldo()
    }

    class Alerta {
        -str tipo
        -str mensagem
        -date data
        +emitir()
        +__str__()
    }

    class GerenciadorAlertas {
        -list alertas
        +registrar()
        +verificar_alto_valor()
        +verificar_limite()
        +verificar_deficit()
    }

    class Relatorio {
        -list lancamentos
        +gerar()
    }


    Lancamento <|-- Receita
    Lancamento <|-- Despesa

    Categoria "1" --> "0..*" Lancamento : possui
    OrcamentoMensal "1" --> "0..*" Lancamento : agrupa

    Lancamento --> Categoria : pertence

    Despesa --> Alerta : pode gerar
    OrcamentoMensal --> Alerta : pode gerar

    GerenciadorAlertas --> Alerta : registra
    GerenciadorAlertas --> Despesa : verifica
    GerenciadorAlertas --> OrcamentoMensal : verifica

    Relatorio --> Lancamento : utiliza
```
