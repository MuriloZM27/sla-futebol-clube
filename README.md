📚 Sistema de Empréstimo e Devolução

Disciplina: Teste de Integração — ETSOF-6
Equipe: Grupo 3 – Empréstimo e Devolução
Tecnologia: Python 3 + Pytest
Metodologia: Test-Driven Development (TDD)

🎯 Objetivo

Implementar o módulo de Empréstimo e Devolução seguindo a metodologia TDD (Red → Green → Refactor) e garantir sua integração com os demais módulos:

Equipe 1 → Usuários (UserService)

Equipe 2 → Catálogo (CatalogService)

Equipe 3 → Empréstimo e Devolução

O foco é evidenciar o processo de TDD por meio dos commits no GitHub e demonstrar a cobertura de testes unitários e de contrato.

🧩 Estrutura do Projeto
emprestimo_devolucao/
│
├── src/
│ └── emprestimo/
│ ├── domain.py # Entidade Loan + helpers de serialização
│ ├── service.py # Lógica principal de empréstimo/devolução
│ └── adapters/
│ ├── users_http.py # Adapter de integração com o serviço de Usuários
│ └── catalog_http.py # Adapter de integração com o serviço de Catálogo
│
├── tests/
│ ├── unit/
│ │ ├── contract/ # Testes de contrato (integração)
│ │ │ ├── test_user_contract.py
│ │ │ ├── test_catalog_contract.py
│ │ │ ├── test_loan_dto_contract.py
│ │ │ └── test_flow_side_effects.py
│ │ ├── test_loan_creation.py
│ │ ├── test_return_book.py
│ │ ├── test_limits.py
│ │ ├── test_edge_cases.py
│ │ └── ...
│ ├── conftest.py
│ └── pytest.ini
│
├── requirements.txt
└── README.md

⚙️ Instalação e Execução
1️⃣ Criar e ativar o ambiente virtual
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

2️⃣ Instalar dependências
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

3️⃣ Executar todos os testes
python -m pytest -q

🧪 Estratégia de Testes
🔴 Red

Criar o teste que falha (ex: função ou classe inexistente).

Comitar:

git commit -m "[TDD red] <descrição do teste>"

🟢 Green

Implementar o código mínimo para passar o teste.

Comitar:

git commit -m "[TDD green] <descrição da implementação>"

🟡 Refactor

Melhorar a estrutura sem alterar o comportamento.

Comitar:

git commit -m "[TDD refactor] <descrição da melhoria>"

🧩 Testes Implementados
🔹 Testes Unitários (10+)

Criação de empréstimo válido e inválido.

Devolução e tratamento de empréstimo inexistente.

Limite de empréstimos ativos.

Casos de borda e ordenação de resultados.

🔹 Testes de Contrato (5)
Contrato	Descrição
UserService	Verifica campos e tipos retornados por get_user
CatalogService	Garante formato e validade dos campos get_book
Coerência CatalogService	is_available() reflete o status de get_book()
Loan DTO	Garante serialização ISO-8601 e campos do objeto Loan
Fluxo	Verifica side-effects (mark_loaned, mark_available) no Catálogo
🔗 Integração entre Equipes
Módulo	Responsável	Integração via
Usuário	Equipe 1	UsersHTTP (get_user, is_active)
Catálogo	Equipe 2	CatalogHTTP (get_book, is_available, mark_*)
Empréstimo/Devolução	Equipe 3	LoanService (usa os dois adapters)

Os adapters foram criados para facilitar a futura integração via HTTP, sem depender de rede durante os testes.

🚀 Automação (CI/CD — GitHub Actions)

Crie o arquivo .github/workflows/tests.yml:

name: Run Pytest

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q

✅ Status Final do Projeto

 Ambiente virtual configurado

 Testes unitários e de contrato implementados

 Histórico TDD com commits RED/GREEN

 Integração entre módulos garantida via adapters

 CI configurado no GitHub Actions