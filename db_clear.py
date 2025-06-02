import sqlite3

# Set database file here
DB_FILE = 'data/finance_tracker.db'


def clear_table(table_name):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()
    conn.close()
    print(f"Cleared table: {table_name}")


if __name__ == "__main__":
    # List the tables you want to clear here
    tables_to_clear = [
        'income_sources',
        # 'recurring_expenses',
        # 'daily_expenses'
        # Add 'categories' if you want to reset that too
    ]

    for table in tables_to_clear:
        clear_table(table)

    print("All selected tables cleared!")
