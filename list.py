import customtkinter as ctk
from database import get_connection


def display_list_data(parent_frame):
    # --- Clear old widgets ---
    for widget in parent_frame.winfo_children():
        widget.destroy()

    field_padx = 10
    section_pady = 10

    # --- Combined scrollable box ---
    list_box = ctk.CTkTextbox(parent_frame, wrap='none')
    list_box.pack(
        anchor="w", padx=field_padx, pady=section_pady,
        expand=True, fill="both"
    )
    list_box.configure(state="normal")

    # --- Add Income Section ---
    list_box.insert("end", "=== Income Entries ===\n")
    load_data_into_box(
        list_box,
        'income_sources',
        ['source_name', 'amount', 'date_added']
    )

    # --- Add Recurring Expenses Section ---
    list_box.insert("end", "\n=== Recurring Expenses ===\n")
    load_data_into_box(
        list_box,
        'recurring_expenses',
        ['name', 'amount', 'categories_id', 'date_added']
    )

    # --- Add One-Off Expenses Section ---
    list_box.insert("end", "\n=== One-Off Expenses ===\n")
    load_data_into_box(
        list_box,
        'daily_expenses',
        ['name', 'amount', 'categories_id', 'date_added']
    )

    list_box.configure(state="disabled")


def load_data_into_box(box, table, columns):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
    except Exception as e:
        rows = []
        print(f"Error fetching {table}: {e}")

    conn.close()

    # Skip the first column (id)
    column_headers = " | ".join(columns) + "\n"
    box.insert("end", column_headers)
    box.insert("end", "-" * len(column_headers) + "\n")

    for row in rows:
        trimmed_row = row[1:]  # Skip the id
        line = " | ".join(str(item) for item in trimmed_row) + "\n"
        box.insert("end", line)
