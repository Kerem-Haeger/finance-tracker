import sqlite3

# Connect (will create file if not present)
conn = sqlite3.connect('data/finance_tracker.db')
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

# Create tables, if not present
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS income_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    amount REAL NOT NULL,
    date_added TEXT NOT NULL);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS daily_expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    categories_id INTEGER NOT NULL,
    date_added TEXT NOT NULL,
    FOREIGN KEY (categories_id) REFERENCES categories(id));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recurring_expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    categories_id INTEGER NOT NULL,
    date_added TEXT NOT NULL,
    FOREIGN KEY (categories_id) REFERENCES categories(id));
''')

conn.commit()

conn.close()
