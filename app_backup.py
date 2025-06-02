import tkinter as tk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from database import (
    add_income,
    add_daily_expense,
    add_recurring_expense,
    get_total_income,
    get_total_recurring_expenses,
    get_daily_expenses_by_month
)

root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("800x600")
root.configure(bg="#f0f4f8")

current_month = "2025-06"


def validate_amount(new_value):
    if new_value == "" or new_value.replace('.', '', 1).isdigit():
        return True
    return False


def update_dashboard():
    total_income = get_total_income()
    total_recurring = get_total_recurring_expenses()
    total_daily = get_daily_expenses_by_month(current_month)
    remaining = total_income - total_recurring - total_daily

    for widget in content_frame.winfo_children():
        widget.destroy()

    dashboard_label = tk.Label(
        content_frame,
        text=f"Dashboard View\n\n"
             f"Total Income: £{total_income}\n"
             f"Total Monthly Expenses: £{total_recurring}\n"
             f"Remaining Balance: £{remaining}",
        font=("Helvetica", 14),
        bg="#e0e0e0",
        width=60,
        height=20,
        relief='ridge'
    )
    dashboard_label.pack(expand=True)


def open_add_income_popup():
    popup = tk.Toplevel(root)
    popup.title("Add Income")

    vcmd = root.register(validate_amount)

    tk.Label(popup, text="Source Name:").pack()
    name_entry = tk.Entry(popup)
    name_entry.pack()

    tk.Label(popup, text="Amount:").pack()
    amount_entry = tk.Entry(popup, validate="key",
                            validatecommand=(vcmd, '%P'))
    amount_entry.pack()

    tk.Label(popup, text="Date:").pack()
    date_entry = DateEntry(
        popup, width=12,
        background='gray',
        foreground='white',
        borderwidth=2,
        date_pattern='yyyy-mm-dd'
    )
    date_entry.pack()

    def submit():
        name = name_entry.get()
        amount = float(amount_entry.get())
        date = date_entry.get()
        add_income(name, amount, date)
        popup.destroy()
        update_dashboard()

    tk.Button(popup, text="Submit", command=submit).pack(pady=5)


def open_add_expense_popup():
    popup = tk.Toplevel(root)
    popup.title("Add Expense")

    vcmd = root.register(validate_amount)

    tk.Label(popup, text="Expense Name:").pack()
    name_entry = tk.Entry(popup)
    name_entry.pack()

    tk.Label(popup, text="Amount:").pack()
    amount_entry = tk.Entry(popup, validate="key",
                            validatecommand=(vcmd, '%P'))
    amount_entry.pack()

    tk.Label(popup, text="Category ID:").pack()
    category_entry = tk.Entry(popup)
    category_entry.pack()

    tk.Label(popup, text="Date:").pack()
    date_entry = DateEntry(
        popup, width=12,
        background='gray',
        foreground='white',
        borderwidth=2,
        date_pattern='yyyy-mm-dd'
    )
    date_entry.pack()

    tk.Label(popup, text="Expense Type:").pack()
    expense_type = tk.StringVar(value="None")
    submit_button = tk.Button(popup, text="Submit", state="disabled")

    def enable_submit():
        if expense_type.get():
            submit_button.config(state="normal")

    tk.Radiobutton(
        popup, text="One-off (Daily)",
        variable=expense_type,
        value="Daily",
        command=enable_submit
    ).pack()
    tk.Radiobutton(
        popup,
        text="Monthly/Recurring",
        variable=expense_type,
        value="Recurring",
        command=enable_submit
    ).pack()

    def submit():
        name = name_entry.get()
        amount = float(amount_entry.get())
        category_id = int(category_entry.get())
        date = date_entry.get()

        if expense_type.get() == "Daily":
            add_daily_expense(name, amount, category_id, date)
        else:
            add_recurring_expense(name, amount, category_id, date)

        popup.destroy()
        update_dashboard()

    submit_button.config(command=submit)
    submit_button.pack(pady=5)


def open_menu():
    menu_popup = tk.Toplevel(root)
    menu_popup.title("Menu")

    tk.Button(
        menu_popup,
        text="Add Income",
        command=open_add_income_popup
    ).pack(pady=5)
    tk.Button(
        menu_popup,
        text="Add Expense",
        command=open_add_expense_popup
    ).pack(pady=5)


def switch_to_graph_view():
    for widget in content_frame.winfo_children():
        widget.destroy()

    income = get_total_income()
    recurring = get_total_recurring_expenses()
    daily = get_daily_expenses_by_month(current_month)

    labels = ['Recurring Expenses', 'Daily Expenses', 'Remaining']
    values = [recurring, daily, income - recurring - daily]

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title("Income vs Expenses")

    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True)


def switch_to_table_view():
    update_dashboard()


# --- Layout Frames ---
header_frame = tk.Frame(root, bg="#f0f4f8")
header_frame.pack(fill='x', pady=10)

content_frame = tk.Frame(root, bg="#f0f4f8")
content_frame.pack(expand=True, fill='both')

footer_frame = tk.Frame(root, bg="#f0f4f8")
footer_frame.pack(pady=10)

# --- Header ---
header_label = tk.Label(
    header_frame,
    text="Welcome to your Finance Tracker!",
    font=("Helvetica", 18),
    bg="#f0f4f8"
)
header_label.pack(side='left', padx=20)

menu_button = tk.Button(
    header_frame,
    text="☰",
    font=("Helvetica", 16),
    command=open_menu
)
menu_button.pack(side='right', padx=20)

# --- Navigation Arrows ---
prev_button = tk.Button(
    footer_frame,
    text="←",
    font=("Helvetica", 14),
    command=switch_to_graph_view
)
prev_button.pack(side='left', padx=40)

next_button = tk.Button(
    footer_frame,
    text="→",
    font=("Helvetica", 14),
    command=switch_to_table_view
)
next_button.pack(side='right', padx=40)

# --- Initialize dashboard ---
update_dashboard()

root.mainloop()
