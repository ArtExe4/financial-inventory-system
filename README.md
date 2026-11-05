# 💰 Controle Financeiro & Gestão de Estoque (CLI ERP)

Sistema integrado de controle de fluxo de caixa e inventário desenvolvido em **Python** com persistência em banco de dados relacional (**SQL**) e geração automatizada de relatórios gerenciais em **PDF**.

---

## ⚙️ Funcionalidades Principais

- **Gestão Financeira (Receitas e Despesas):** Cadastro categorizado de movimentações, cálculo automático de saldo líquido e filtragem dinâmica por período mensal (`YYYY-MM`).
- **Controle de Estoque Inteligente:** Registro de produtos, movimentação de entradas/saídas com validação de saldo e **alerta automático em tempo real** para produtos abaixo do estoque mínimo.
- **Segurança e Integridade de Dados:** Consultas SQL parametrizadas (*Prepared Statements*) prevenindo *SQL Injection* e restrições de integridade (`CHECK` e `UNIQUE`) diretamente no banco de dados.
- **Exportação Gerencial em PDF:** Geração de relatórios formatados com resumo financeiro, tabela de transações e listagem de itens em estoque crítico utilizando `fpdf2`.
- **Modo Demonstração (*Seed Data*):** Opção integrada no menu para popular o banco instantaneamente com dados de teste.

---

## 📂 Estrutura do Projeto

* `database.py` — Camada de persistência SQL, criação de tabelas e queries de negócio
* `pdf_generator.py` — Motor de renderização e estilização dos relatórios em PDF
* `main.py` — Interface interativa de linha de comando (CLI) com tabelas formatadas
* `requirements.txt` — Dependências externas do projeto

---

## 🚀 Como Executar Localmente

1. **Clone o repositório:**
   `git clone https://github.com/ArtExe4/financial-inventory-system.git`
   `cd financial-inventory-system`

2. **Instale as dependências:**
   `pip install -r requirements.txt`

3. **Execute o sistema:**
   `python main.py`

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Banco de Dados:** SQLite3 (SQL Relacional)
- **Bibliotecas:** `fpdf2` (Relatórios PDF), `tabulate` (Tabelas CLI)