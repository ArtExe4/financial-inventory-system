import sqlite3
from datetime import datetime

DB_NAME = "erp_system.db"


def get_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Inicializa as tabelas de Transações Financeiras e Estoque usando SQL puro."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Tabela de Controle Financeiro (Receitas e Despesas)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('Receita', 'Despesa')),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                date TEXT NOT NULL
            )
        """)

        # Tabela de Controle de Estoque
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL DEFAULT 0,
                min_stock INTEGER NOT NULL DEFAULT 5,
                unit_price REAL NOT NULL CHECK(unit_price >= 0)
            )
        """)
        conn.commit()


# ==================== FUNÇÕES FINANCEIRAS ====================

def add_transaction(t_type: str, category: str, description: str, amount: float, date_str: str = None):
    """Registra uma nova Receita ou Despesa."""
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (type, category, description, amount, date)
            VALUES (?, ?, ?, ?, ?)
        """, (t_type, category, description, amount, date_str))
        conn.commit()


def get_transactions_by_month(year_month: str = None):
    """Retorna transações filtradas por mês (formato YYYY-MM) ou todas se não informado."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if year_month:
            cursor.execute("""
                SELECT id, type, category, description, amount, date
                FROM transactions
                WHERE strftime('%Y-%m', date) = ?
                ORDER BY date DESC
            """, (year_month,))
        else:
            cursor.execute("""
                SELECT id, type, category, description, amount, date
                FROM transactions
                ORDER BY date DESC
            """)
        return cursor.fetchall()


def get_financial_summary(year_month: str = None):
    """Calcula o total de receitas, despesas e saldo final."""
    rows = get_transactions_by_month(year_month)
    income = sum(r[4] for r in rows if r[1] == "Receita")
    expense = sum(r[4] for r in rows if r[1] == "Despesa")
    return {
        "receitas": income,
        "despesas": expense,
        "saldo": income - expense
    }


# ==================== FUNÇÕES DE ESTOQUE ====================

def add_product(name: str, quantity: int, min_stock: int, unit_price: float):
    """Cadastra um novo produto no estoque."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, quantity, min_stock, unit_price)
            VALUES (?, ?, ?, ?)
        """, (name, quantity, min_stock, unit_price))
        conn.commit()


def update_stock(product_id: int, delta: int):
    """Atualiza a quantidade de um produto (+ para entrada, - para saída)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Produto não encontrado.")
        if row[0] + delta < 0:
            raise ValueError("Estoque insuficiente para essa saída.")

        cursor.execute("""
            UPDATE products
            SET quantity = quantity + ?
            WHERE id = ?
        """, (delta, product_id))
        conn.commit()


def get_all_products():
    """Lista todos os produtos cadastrados."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, min_stock, unit_price FROM products ORDER BY name")
        return cursor.fetchall()


def get_low_stock_alerts():
    """Retorna produtos com quantidade abaixo ou igual ao estoque mínimo definido."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, quantity, min_stock
            FROM products
            WHERE quantity <= min_stock
            ORDER BY quantity ASC
        """)
        return cursor.fetchall()