import tkinter as tk
from database import (
    add_income,
    get_total_income,
    get_total_recurring_expenses,
    get_daily_expenses_by_month
)

# --- Initialize root window ---
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("600x400")

current_month = "2025-06"  # hardcoded for now

# --- Define dashboard labels (will be updated later) ---
label = tk.Label(root, text="Welcome to your Finance Tracker!",
                 font=("Helvetica", 16))
label.pack(pady=20)

income_label = tk.Label(root, font=("Helvetica", 14))
income_label.pack(pady=5)

recurring_label = tk.Label(root, font=("Helvetica", 14))
recurring_label.pack(pady=5)

remaining_label = tk.Label(root, font=("Helvetica", 14, "bold"))
remaining_label.pack(pady=10)


# --- Define function to update dashboard labels ---
def update_dashboard():
    total_income = get_total_income()
    total_recurring = get_total_recurring_expenses()
    total_daily = get_daily_expenses_by_month(current_month)
    remaining = total_income - total_recurring - total_daily

    income_label.config(text=f"Total Income: £{total_income}")
    recurring_label.config(text=f"Total Monthly Expenses: £{total_recurring}")
    remaining_label.config(text=f"Remaining Balance: £{remaining}")


# --- Define popup for adding income ---
def open_add_income_popup():
    popup = tk.Toplevel(root)
    popup.title("Add Income")

    tk.Label(popup, text="Source Name:").pack()
    source_entry = tk.Entry(popup)
    source_entry.pack()

    tk.Label(popup, text="Amount:").pack()
    amount_entry = tk.Entry(popup)
    amount_entry.pack()

    tk.Label(popup, text="Date (YYYY-MM-DD):").pack()
    date_entry = tk.Entry(popup)
    date_entry.pack()

    def submit():
        source = source_entry.get()
        amount = float(amount_entry.get())
        date = date_entry.get()
        add_income(source, amount, date)
        popup.destroy()  # close popup
        update_dashboard()  # refresh dashboard

    submit_button = tk.Button(popup, text="Submit", command=submit)
    submit_button.pack(pady=5)


# --- Build the GUI ---
add_income_button = tk.Button(root, text="Add Income",
                              command=open_add_income_popup)
add_income_button.pack(pady=10)

# --- Initial dashboard update ---
update_dashboard()

root.mainloop()
