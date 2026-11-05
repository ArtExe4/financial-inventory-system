from tabulate import tabulate
import database as db
from pdf_generator import export_report_to_pdf


def display_stock_alerts():
    """Exibe automaticamente avisos de produtos com estoque crítico no topo do menu."""
    alerts = db.get_low_stock_alerts()
    if alerts:
        print("\n" + "=" * 60)
        print("⚠️  ALERTA AUTOMÁTICO DE ESTOQUE BAIXO ⚠️")
        for p_id, name, qty, min_qty in alerts:
            print(f" -> Produto [{p_id}] '{name}': apenas {qty} un. (Mínimo: {min_qty} un.)")
        print("=" * 60)


def seed_demo_data():
    """Popula o banco com dados iniciais de exemplo sem duplicar se já existirem."""
    try:
        db.add_product("Mouse Gamer Sem Fio", 12, 5, 189.90)
        db.add_product("Teclado Mecanico Switch Blue", 3, 5, 249.90)  # Vai disparar alerta!
        db.add_product("Monitor IPS 24 Pol 144Hz", 2, 4, 899.00)     # Vai disparar alerta!

        db.add_transaction("Receita", "Vendas", "Venda de 2x Mouse Gamer", 379.80, "2026-11-02")
        db.add_transaction("Receita", "Servicos", "Manutencao Preventiva PC", 150.00, "2026-11-04")
        db.add_transaction("Despesa", "Fornecedores", "Reposicao de Cabos Cat6", 95.50, "2026-11-05")
        print("\n✅ Dados de demonstração carregados com sucesso!")
    except Exception:
        print("\nℹ️ Os dados de demonstração já foram carregados anteriormente!")


def main():
    db.init_db()

    while True:
        display_stock_alerts()
        print("\n📊 SISTEMA INTEGRADO: CONTROLE FINANCEIRO & ESTOQUE")
        print("1. Cadastrar Receita / Despesa")
        print("2. Relatório Financeiro (Geral ou Filtro por Mês)")
        print("3. Cadastrar Novo Produto no Estoque")
        print("4. Listar Estoque e Registrar Entrada/Saída")
        print("5. Exportar Relatório Completo em PDF")
        print("6. Carregar Dados de Demonstração (Teste Rápido)")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            t_type = "Receita" if input("Tipo (1-Receita / 2-Despesa): ").strip() == "1" else "Despesa"
            category = input("Categoria (ex: Vendas, Aluguel, Fornecedores): ").strip()
            desc = input("Descrição: ").strip()
            try:
                amount = float(input("Valor (R$): ").replace(",", "."))
                date_str = input("Data YYYY-MM-DD (deixe vazio para hoje): ").strip()
                db.add_transaction(t_type, category, desc, amount, date_str or None)
                print("✅ Transação registrada com sucesso!")
            except ValueError as e:
                print(f"❌ Erro ao registrar: {e}")

        elif opcao == "2":
            ym = input("Filtrar por Ano-Mês (ex: 2026-11) ou Enter para Todos: ").strip()
            rows = db.get_transactions_by_month(ym or None)
            summary = db.get_financial_summary(ym or None)

            print("\n--- Histórico de Transações ---")
            if rows:
                print(tabulate(rows, headers=["ID", "Tipo", "Categoria", "Descrição", "Valor (R$)", "Data"], tablefmt="grid", floatfmt=".2f"))
            else:
                print("Nenhuma movimentação encontrada.")

            print(f"\n💰 Receitas: R$ {summary['receitas']:.2f} | 💸 Despesas: R$ {summary['despesas']:.2f} | ⚖️ Saldo: R$ {summary['saldo']:.2f}")

        elif opcao == "3":
            name = input("Nome do Produto: ").strip()
            try:
                qty = int(input("Quantidade Inicial: "))
                min_s = int(input("Estoque Mínimo para Alerta: "))
                price = float(input("Preço Unitário (R$): ").replace(",", "."))
                db.add_product(name, qty, min_s, price)
                print("✅ Produto cadastrado com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao cadastrar produto: {e}")

        elif opcao == "4":
            products = db.get_all_products()
            print("\n--- Posição Atual de Estoque ---")
            if products:
                print(tabulate(products, headers=["ID", "Produto", "Qtd Atual", "Estoque Mín.", "Preço Un. (R$)"], tablefmt="grid", floatfmt=".2f"))
                sub = input("\nDeseja movimentar algum item? (s/n): ").strip().lower()
                if sub == "s":
                    try:
                        p_id = int(input("ID do Produto: "))
                        delta = int(input("Quantidade (+ para Entrada, - para Saída, ex: -2): "))
                        db.update_stock(p_id, delta)
                        print("✅ Estoque atualizado!")
                    except Exception as e:
                        print(f"❌ Erro: {e}")
            else:
                print("Nenhum produto cadastrado.")

        elif opcao == "5":
            ym = input("Período do PDF (ex: 2026-11) ou Enter para Geral: ").strip()
            rows = db.get_transactions_by_month(ym or None)
            summary = db.get_financial_summary(ym or None)
            alerts = db.get_low_stock_alerts()
            filename = export_report_to_pdf(rows, summary, alerts, period_label=ym or "Geral")
            print(f"📄 Relatório exportado com sucesso no arquivo: {filename}")

        elif opcao == "6":
            seed_demo_data()

        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()