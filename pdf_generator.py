from fpdf import FPDF
from datetime import datetime


class FinancialPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.cell(0, 10, "Relatorio Gerencial - Financeiro & Estoque", border=False, ln=True, align="C")
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 6, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}} - Crafted by Art", align="C")


def export_report_to_pdf(transactions, summary, low_stock_items, period_label="Geral", filename="relatorio_financeiro.pdf"):
    """Gera um arquivo PDF formatado com o resumo financeiro, movimentações e alertas de estoque."""
    pdf = FinancialPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # 1. Resumo Financeiro do Período
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"1. Resumo Financeiro (Periodo: {period_label})", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Total de Receitas: R$ {summary['receitas']:.2f}", ln=True)
    pdf.cell(0, 6, f"Total de Despesas: R$ {summary['despesas']:.2f}", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, f"Saldo Liquido: R$ {summary['saldo']:.2f}", ln=True)
    pdf.ln(6)

    # 2. Tabela de Movimentações
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "2. Historico de Transacoes", ln=True)

    # Cabeçalho da Tabela
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(25, 7, "Data", border=1, fill=True, align="C")
    pdf.cell(25, 7, "Tipo", border=1, fill=True, align="C")
    pdf.cell(35, 7, "Categoria", border=1, fill=True, align="C")
    pdf.cell(70, 7, "Descricao", border=1, fill=True, align="L")
    pdf.cell(35, 7, "Valor (R$)", border=1, fill=True, align="R", ln=True)

    # Linhas da Tabela
    pdf.set_font("Helvetica", "", 9)
    if not transactions:
        pdf.cell(190, 7, "Nenhuma transacao registrada neste periodo.", border=1, ln=True, align="C")
    else:
        for t in transactions:
            _, t_type, category, desc, amount, date_str = t
            pdf.cell(25, 7, str(date_str), border=1, align="C")
            pdf.cell(25, 7, str(t_type), border=1, align="C")
            pdf.cell(35, 7, str(category)[:18], border=1, align="C")
            pdf.cell(70, 7, str(desc)[:38], border=1, align="L")
            pdf.cell(35, 7, f"{amount:.2f}", border=1, align="R", ln=True)

    pdf.ln(8)

    # 3. Alertas de Estoque Baixo
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "3. Alertas de Estoque Critico", ln=True)
    pdf.set_font("Helvetica", "", 10)
    if not low_stock_items:
        pdf.cell(0, 6, "Todos os produtos estao com estoque acima do limite minimo.", ln=True)
    else:
        for item in low_stock_items:
            p_id, name, qty, min_qty = item
            pdf.cell(0, 6, f"[ALERTA] ID {p_id} - {name}: {qty} un. em estoque (Minimo exigido: {min_qty} un.)", ln=True)

    pdf.output(filename)
    return filename