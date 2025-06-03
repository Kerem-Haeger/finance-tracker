import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from database import (
    get_total_income,
    get_daily_expenses_by_month,
    get_recurring_expenses_by_category,
    get_oneoff_expenses_by_category
)


def display_overview_chart(parent_frame):
    # --- Get data ---
    total_income = get_total_income()
    total_oneoff = get_daily_expenses_by_month(
        datetime.date.today().strftime("%Y-%m")
    )
    oneoff_by_cat = get_oneoff_expenses_by_category()
    recurring_by_cat = get_recurring_expenses_by_category()
    total_recurring = sum(amount for _, amount in recurring_by_cat)
    total_oneoff_cats = sum(amount for _, amount in oneoff_by_cat)
    remaining = total_income - (total_recurring + total_oneoff_cats)

    # --- Prepare data ---
    labels = []
    sizes = []
    colors = []
    explode = []

    # Helper: generate shades
    def get_color_shades(colormap, n):
        return [colormap(i / (n + 1)) for i in range(1, n + 1)]

    # Remaining (single green shade)
    if remaining > 0:
        labels.append(f"Remaining (£{remaining:.2f})")
        sizes.append(remaining)
        colors.append("#66bb6a")  # solid green
        explode.append(0.05)

    # Recurring: dynamic blue shades
    rec_colors = get_color_shades(cm.Blues, len(recurring_by_cat))
    for i, (category, amount) in enumerate(recurring_by_cat):
        labels.append(f"Recurring: {category} (£{amount:.2f})")
        sizes.append(amount)
        colors.append(rec_colors[i])
        explode.append(0.03)

    # One-off: dynamic red shades
    oneoff_colors = get_color_shades(cm.Reds, len(oneoff_by_cat))
    for i, (category, amount) in enumerate(oneoff_by_cat):
        labels.append(f"One-Off: {category} (£{amount:.2f})")
        sizes.append(amount)
        colors.append(oneoff_colors[i])
        explode.append(0.03)

    # --- Create figure ---
    fig, ax = plt.subplots(figsize=(7, 7))

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f"£{val}"
        return my_autopct

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct=make_autopct(sizes),
        startangle=140,
        colors=colors,
        explode=explode,
        pctdistance=0.85
    )

    ax.legend(
        wedges, labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Donut hole
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig.gca().add_artist(centre_circle)

    ax.axis("equal")
    plt.tight_layout()

    # --- Embed chart ---
    for widget in parent_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill="both")

    plt.close(fig)
