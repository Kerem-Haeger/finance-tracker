import tkinter as tk
from database import (
    get_total_income,
    get_total_recurring_expenses,
    get_daily_expenses_by_month
)


root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("600x400")

total_income = get_total_income()
total_recurring = get_total_recurring_expenses()
total_daily = get_daily_expenses_by_month("2025-06")  # hardcoded for now

remaining = total_income - total_recurring - total_daily

label = tk.Label(root, text="Welcome to your Finance Tracker!",
                 font=("Helvetica", 16))
label.pack(pady=20)

income_label = tk.Label(root, text=f"Total Income: £{total_income}",
                        font=("Helvetica", 14))
income_label.pack(pady=5)

recurring_label = tk.Label(root,
                           text=f"Total Monthly Expenses: £{total_recurring}",
                           font=("Helvetica", 14))
recurring_label.pack(pady=5)

remaining_label = tk.Label(root, text=f"Remaining Balance: £{remaining}",
                           font=("Helvetica", 14, "bold"))
remaining_label.pack(pady=10)

root.mainloop()
