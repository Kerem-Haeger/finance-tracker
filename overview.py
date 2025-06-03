import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from database import (
    get_total_income,
    get_total_recurring_expenses,
    get_daily_expenses_by_month,
    get_recurring_expenses_by_category
)


def display_overview_chart(parent_frame):
    # --- Get data ---
    total_income = get_total_income()
    total_oneoff = get_daily_expenses_by_month(
        datetime.date.today().strftime("%Y-%m")
    )
    recurring_by_cat = get_recurring_expenses_by_category()
    total_recurring = sum(amount for _, amount in recurring_by_cat)

    remaining = total_income - (total_oneoff + total_recurring)

    # --- Prepare pie chart data ---
    labels = ["Remaining"]
    sizes = [remaining]
    colors = ["#66bb6a"]  # green

    # Add recurring categories
    for category, amount in recurring_by_cat:
        labels.append(f"Recurring: {category}")
        sizes.append(amount)
        colors.append("#42a5f5")  # blue

    # Add one-off as single slice
    if total_oneoff > 0:
        labels.append("One-Off Expenses")
        sizes.append(total_oneoff)
        colors.append("#ef5350")  # red

    # --- Create figure ---
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    # --- Embed chart in Tkinter frame ---
    for widget in parent_frame.winfo_children():
        widget.destroy()  # Clear old chart if present

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill="both")

    plt.close(fig)
