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
