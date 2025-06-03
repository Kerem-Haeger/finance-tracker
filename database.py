import sqlite3


def get_connection():
    conn = sqlite3.connect('data/finance_tracker.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def add_income(source_name, amount, date_added):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO income_sources (source_name, amount, date_added)
        VALUES (?, ?, ?)
        ''',
        (source_name, amount, date_added)
    )

    conn.commit()
    conn.close()
    print(f"Added income source: {source_name} (£{amount}) on {date_added}")


def add_recurring_expense(name, amount, categories_id, date_added):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
    INSERT INTO recurring_expenses (name, amount, categories_id, date_added)
    VALUES (?,?,?,?)
        ''',
        (name, amount, categories_id, date_added)
    )

    conn.commit()
    conn.close()
    print(f'''Added recurring expense: {name} (£{amount}) on {date_added},
        labeled {categories_id}''')


def add_daily_expense(name, amount, categories_id, date_added):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
    INSERT INTO daily_expenses (name, amount, categories_id, date_added)
    VALUES (?,?,?,?)
        ''',
        (name, amount, categories_id, date_added)
    )

    conn.commit()
    conn.close()
    print(f'''Added daily expense: {name} (£{amount}) on {date_added},
        labeled {categories_id}''')


def add_category(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()
    print(f"Category added: {name}")


def get_total_income():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM income_sources;")
    result = cursor.fetchone()[0]

    conn.close()

    total = result if result is not None else 0
    return total


def get_total_recurring_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM recurring_expenses;")
    result = cursor.fetchone()[0]

    conn.close()

    total = result if result is not None else 0
    return total


def get_recurring_expenses_by_category():
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT categories.name, SUM(recurring_expenses.amount)
        FROM recurring_expenses
        JOIN categories ON recurring_expenses.categories_id = categories.id
        GROUP BY categories.name;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results  # List of (category_name, total_amount)


def get_daily_expenses_by_month(year_month):
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
                SELECT SUM(amount) FROM daily_expenses WHERE date_added LIKE ?;
                '''
    pattern = year_month + "%"

    cursor.execute(query, (pattern,))
    result = cursor.fetchone()[0]

    conn.close()

    total = result if result is not None else 0
    return total


def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM categories;")
    rows = cursor.fetchall()

    conn.close()

    return rows
