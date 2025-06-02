import sqlite3


def check_database():
    # Connect to DB
    conn = sqlite3.connect('data/finance_tracker.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    print("Connected to database.")

    print("\n Listing tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        for table in tables:
            print(f"-{table[0]}")
        else:
            print("No tables found.")

    for table in tables:
        table_name = table[0]
        print(f"\nChecking data in table: {table_name}")
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 50;")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No data found.")
        except sqlite3.Error as e:
            print(f"Error querying table {table_name}: {e}")

    conn.close()
    print("\nDatabase check complete.")


if __name__ == "__main__":
    check_database()
