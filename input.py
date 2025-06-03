import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
from database import (
    add_income,
    add_recurring_expense,
    add_daily_expense
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

    # --- Layout settings ---
    field_padx = 10  # horizontal gap from left edge
    label_pady = 1   # small gap between label and input
    field_pady = 8   # vertical gap between field blocks
    large_pady = 15  # extra gap before submit button

    # --- Section header ---
    section_label = ctk.CTkLabel(
        parent_frame, text="Add An Income", font=ctk.CTkFont(weight="bold")
    )
    section_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    # --- Amount input ---
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

    # --- Name/reference input ---
    name_var = ctk.StringVar(value="Salary")
    name_label = ctk.CTkLabel(
        parent_frame, text="Reference Name (max 20 chars):"
    )
    name_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    name_entry = ctk.CTkEntry(
        parent_frame, textvariable=name_var
    )
    name_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    # --- Date picker ---
    date_label = ctk.CTkLabel(
        parent_frame, text="Date (optional):"
    )
    date_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    date_entry = DateEntry(parent_frame, width=12)
    date_entry.pack(anchor="w", padx=field_padx, pady=(0, large_pady))

    # --- Submit button ---
    submit_btn = ctk.CTkButton(
        parent_frame, text="Add Income", command=submit_income
    )
    submit_btn.pack(anchor="w", padx=field_padx, pady=(0, field_pady))


def setup_recurring_form(parent_frame):
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

        if not amount or not name:
            print("Please fill in all fields.")
            return

        # Placeholder: categories_id set to 1 for now
        add_recurring_expense(name, float(amount), 1, date)
        print(f"Recurring expense saved ({frequency}).")

    # --- Layout settings ---
    field_padx = 10
    label_pady = 1
    field_pady = 8
    large_pady = 15

    # --- Section header ---
    section_label = ctk.CTkLabel(
        parent_frame, text="Add Recurring Expense",
        font=ctk.CTkFont(weight="bold")
    )
    section_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    # --- Amount input ---
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

    # --- Name/reference input ---
    name_var = ctk.StringVar(value="Rent")
    name_label = ctk.CTkLabel(
        parent_frame, text="Reference Name (max 20 chars):"
    )
    name_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    name_entry = ctk.CTkEntry(
        parent_frame, textvariable=name_var
    )
    name_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    # --- Date picker ---
    date_label = ctk.CTkLabel(
        parent_frame, text="Date (optional):"
    )
    date_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    date_entry = DateEntry(parent_frame, width=12)
    date_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    # --- Frequency radio buttons ---
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

    # --- Submit button ---
    submit_btn = ctk.CTkButton(
        parent_frame, text="Add Recurring Expense",
        command=submit_recurring
    )
    submit_btn.pack(anchor="w", padx=field_padx, pady=(large_pady, field_pady))


def setup_oneoff_form(parent_frame):
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

        if not amount or not name:
            print("Please fill in all fields.")
            return

        # Placeholder: categories_id set to 1 for now
        add_daily_expense(name, float(amount), 1, date)
        print("One-off expense saved.")

    # --- Layout settings ---
    field_padx = 10
    label_pady = 2
    field_pady = 8
    large_pady = 15

    # --- Section header ---
    section_label = ctk.CTkLabel(
        parent_frame, text="Add One-Off Expense",
        font=ctk.CTkFont(weight="bold")
    )
    section_label.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    # --- Amount input ---
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

    # --- Name/reference input ---
    name_var = ctk.StringVar(value="Groceries")
    name_label = ctk.CTkLabel(
        parent_frame, text="Reference Name (max 20 chars):"
    )
    name_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    name_entry = ctk.CTkEntry(
        parent_frame, textvariable=name_var
    )
    name_entry.pack(anchor="w", padx=field_padx, pady=(0, field_pady))

    # --- Date picker ---
    date_label = ctk.CTkLabel(
        parent_frame, text="Date (optional):"
    )
    date_label.pack(anchor="w", padx=field_padx, pady=(0, label_pady))

    date_entry = DateEntry(parent_frame, width=12)
    date_entry.pack(anchor="w", padx=field_padx, pady=(0, large_pady))

    # --- Submit button ---
    submit_btn = ctk.CTkButton(
        parent_frame, text="Add One-Off Expense",
        command=submit_oneoff
    )
    submit_btn.pack(anchor="w", padx=field_padx, pady=(0, field_pady))
