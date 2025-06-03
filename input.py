import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
from database import (
    add_income,
    add_recurring_expense,
    add_daily_expense,
    get_all_categories
)


def setup_income_form(parent_frame):

    def validate_amount(new_value):
        if new_value == "":
            return True
        try:
            value = float(new_value)
            if value < 0:
                return False
            parts = new_value.split(".")
            if len(parts) == 2 and len(parts[1]) > 2:
                return False
            return True
        except ValueError:
            return False

    def submit_income():
        amount = amount_var.get()
        name = name_var.get()
        date = date_entry.get_date()

        if not amount or not name:
            print("Please fill in all fields.")
            return

        add_income(name, float(amount), date)
        print("Income entry saved.")

        amount_var.set("")
        name_var.set("")
        date_entry.set_date(datetime.date.today())

        success_label.configure(text="✅ Added!")
        parent_frame.after(2000, lambda: success_label.configure(text=""))

    field_padx = 10
    label_pady = 1
    field_pady = 8
    large_pady = 15

    section_label = ctk.CTkLabel(
        parent_frame, text="Add An Income",
        font=ctk.CTkFont(weight="bold")
    )
    section_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    amount_var = ctk.StringVar()
    amount_label = ctk.CTkLabel(
        parent_frame, text="Amount (£):"
    )
    amount_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    amount_entry = ctk.CTkEntry(
        parent_frame, textvariable=amount_var
    )
    amount_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    vcmd = (parent_frame.register(validate_amount), "%P")
    amount_entry.configure(validate="key", validatecommand=vcmd)

    name_var = ctk.StringVar(value="Salary")
    name_label = ctk.CTkLabel(
        parent_frame, text="Reference Name (max 20 chars):"
    )
    name_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    name_entry = ctk.CTkEntry(
        parent_frame, textvariable=name_var
    )
    name_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    date_label = ctk.CTkLabel(
        parent_frame, text="Date (optional):"
    )
    date_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    date_entry = DateEntry(parent_frame, width=12)
    date_entry.pack(anchor="w", padx=field_padx, pady=(0, large_pady))

    submit_btn = ctk.CTkButton(
        parent_frame, text="Add Income", command=submit_income
    )
    submit_btn.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    success_label = ctk.CTkLabel(
        parent_frame, text="", text_color="green"
    )
    success_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))


def setup_recurring_form(parent_frame):
    categories = get_all_categories()
    category_names = [name for _, name in categories]
    category_id_map = {name: cid for cid, name in categories}

    def validate_amount(new_value):
        if new_value == "":
            return True
        try:
            value = float(new_value)
            if value < 0:
                return False
            parts = new_value.split(".")
            if len(parts) == 2 and len(parts[1]) > 2:
                return False
            return True
        except ValueError:
            return False

    def submit_recurring():
        amount = amount_var.get()
        name = name_var.get()
        date = date_entry.get_date()
        frequency = freq_var.get()
        category = category_var.get()

        if not amount or not name:
            print("Please fill in all fields.")
            return

        category_id = category_id_map[category]
        add_recurring_expense(name, float(amount), category_id, date)
        print(f"Recurring expense saved ({frequency}, Category: {category}).")

        amount_var.set("")
        name_var.set("")
        date_entry.set_date(datetime.date.today())

        success_label.configure(text="✅ Added!")
        parent_frame.after(2000, lambda: success_label.configure(text=""))

    field_padx = 10
    label_pady = 1
    field_pady = 8
    large_pady = 15

    section_label = ctk.CTkLabel(
        parent_frame, text="Add Recurring Expense",
        font=ctk.CTkFont(weight="bold")
    )
    section_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    amount_var = ctk.StringVar()
    amount_label = ctk.CTkLabel(
        parent_frame, text="Amount (£):"
    )
    amount_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    amount_entry = ctk.CTkEntry(
        parent_frame, textvariable=amount_var
    )
    amount_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    vcmd = (parent_frame.register(validate_amount), "%P")
    amount_entry.configure(validate="key", validatecommand=vcmd)

    name_var = ctk.StringVar(value="Rent")
    name_label = ctk.CTkLabel(
        parent_frame, text="Reference Name (max 20 chars):"
    )
    name_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    name_entry = ctk.CTkEntry(
        parent_frame, textvariable=name_var
    )
    name_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    category_label = ctk.CTkLabel(
        parent_frame, text="Category:"
    )
    category_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    category_var = ctk.StringVar(value=category_names[0])
    category_menu = ctk.CTkOptionMenu(
        parent_frame, values=category_names, variable=category_var
    )
    category_menu.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    date_label = ctk.CTkLabel(
        parent_frame, text="Date (optional):"
    )
    date_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    date_entry = DateEntry(parent_frame, width=12)
    date_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    freq_label = ctk.CTkLabel(
        parent_frame, text="Frequency:"
    )
    freq_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    freq_var = ctk.StringVar(value="Monthly")
    for option in ["Monthly", "Weekly", "Yearly"]:
        radio = ctk.CTkRadioButton(
            parent_frame, text=option, variable=freq_var, value=option
        )
        radio.pack(anchor="w", padx=field_padx)

    submit_btn = ctk.CTkButton(
        parent_frame, text="Add Recurring Expense",
        command=submit_recurring
    )
    submit_btn.pack(anchor="w", padx=field_padx, pady=(large_pady, field_pady))

    success_label = ctk.CTkLabel(
        parent_frame, text="", text_color="green"
    )
    success_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))


def setup_oneoff_form(parent_frame):
    categories = get_all_categories()
    category_names = [name for _, name in categories]
    category_id_map = {name: cid for cid, name in categories}

    def validate_amount(new_value):
        if new_value == "":
            return True
        try:
            value = float(new_value)
            if value < 0:
                return False
            parts = new_value.split(".")
            if len(parts) == 2 and len(parts[1]) > 2:
                return False
            return True
        except ValueError:
            return False

    def submit_oneoff():
        amount = amount_var.get()
        name = name_var.get()
        date = date_entry.get_date()
        category = category_var.get()

        if not amount or not name:
            print("Please fill in all fields.")
            return

        category_id = category_id_map[category]
        add_daily_expense(name, float(amount), category_id, date)
        print(f"One-off expense saved (Category: {category}).")

        amount_var.set("")
        name_var.set("")
        date_entry.set_date(datetime.date.today())

        success_label.configure(text="✅ Added!")
        parent_frame.after(2000, lambda: success_label.configure(text=""))

    field_padx = 10
    label_pady = 1
    field_pady = 8
    large_pady = 15

    section_label = ctk.CTkLabel(
        parent_frame, text="Add One-Off Expense",
        font=ctk.CTkFont(weight="bold")
    )
    section_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    amount_var = ctk.StringVar()
    amount_label = ctk.CTkLabel(
        parent_frame, text="Amount (£):"
    )
    amount_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    amount_entry = ctk.CTkEntry(
        parent_frame, textvariable=amount_var
    )
    amount_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    vcmd = (parent_frame.register(validate_amount), "%P")
    amount_entry.configure(validate="key", validatecommand=vcmd)

    name_var = ctk.StringVar(value="Groceries")
    name_label = ctk.CTkLabel(
        parent_frame, text="Reference Name (max 20 chars):"
    )
    name_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    name_entry = ctk.CTkEntry(
        parent_frame, textvariable=name_var
    )
    name_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    category_label = ctk.CTkLabel(
        parent_frame, text="Category:"
    )
    category_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    category_var = ctk.StringVar(value=category_names[0])
    category_menu = ctk.CTkOptionMenu(
        parent_frame, values=category_names, variable=category_var
    )
    category_menu.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    date_label = ctk.CTkLabel(
        parent_frame, text="Date (optional):"
    )
    date_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    date_entry = DateEntry(parent_frame, width=12)
    date_entry.pack(anchor="w", padx=field_padx, pady=(0, large_pady))

    submit_btn = ctk.CTkButton(
        parent_frame, text="Add One-Off Expense",
        command=submit_oneoff
    )
    submit_btn.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    success_label = ctk.CTkLabel(
        parent_frame, text="", text_color="green"
    )
    success_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))
