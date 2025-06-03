import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import (
    get_total_income,
    get_recurring_expenses_by_category,
    get_oneoff_expenses_by_category
)


def display_overview_chart(parent_frame):
    # --- Get data ---
    total_income = get_total_income()
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

    def get_color_shades(colormap, n):
        return [colormap(i / (n + 1)) for i in range(1, n + 1)]

    if remaining > 0:
        labels.append(f"Remaining (£{remaining:.2f})")
        sizes.append(remaining)
        colors.append("#66bb6a")
        explode.append(0.05)

    rec_colors = get_color_shades(cm.Blues, len(recurring_by_cat))
    for i, (category, amount) in enumerate(recurring_by_cat):
        labels.append(f"Recurring: {category} (£{amount:.2f})")
        sizes.append(amount)
        colors.append(rec_colors[i])
        explode.append(0.03)

    oneoff_colors = get_color_shades(cm.Reds, len(oneoff_by_cat))
    for i, (category, amount) in enumerate(oneoff_by_cat):
        labels.append(f"One-Off: {category} (£{amount:.2f})")
        sizes.append(amount)
        colors.append(oneoff_colors[i])
        explode.append(0.03)

    # --- Create figure ---
    fig, ax = plt.subplots(figsize=(8, 8))

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

    # --- Primary legend (categories) ---
    ax.legend(
        wedges, labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5)  # right side, centered vertically
    )

    # --- Secondary legend (totals) ---
    summary_labels = [
        f"Total Income: £{total_income:.2f}",
        f"Total Recurring: £{total_recurring:.2f}"
    ]
    ax.text(
        0, -1.3,  # X=0 (center), Y=-1.3 (below chart)
        "\n".join(summary_labels),
        ha="center", va="center",
        fontsize=10,
        bbox=dict(
            boxstyle="round,pad=0.5",
            edgecolor="gray",
            facecolor="white"
            )
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
