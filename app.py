import customtkinter as ctk
from input import (
    setup_income_form,
    setup_recurring_form,
    setup_oneoff_form
    )
from overview import (
    display_overview_chart
)
from list import display_list_data


# --- Setup window ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Finance Tracker")
app.geometry("800x600")


# --- Frame switching function ---
def show_frame(frame):
    frame.tkraise()


# --- Create content frames ---
overview_frame = ctk.CTkFrame(app)
list_frame = ctk.CTkFrame(app)
add_info_frame = ctk.CTkFrame(app)

for frame in (overview_frame, list_frame, add_info_frame):
    frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


# --- Overview and List placeholders ---
ctk.CTkLabel(overview_frame, text="Overview Section").pack(pady=20)
ctk.CTkLabel(list_frame, text="List Section").pack(pady=20)
display_overview_chart(overview_frame)


# --- Add Info Frame: 3 side-by-side sections ---
income_section = ctk.CTkFrame(add_info_frame)
recurring_section = ctk.CTkFrame(add_info_frame)
oneoff_section = ctk.CTkFrame(add_info_frame)

income_section.pack(side="left", expand=True, fill="both", padx=5, pady=5)
recurring_section.pack(side="left", expand=True, fill="both", padx=5, pady=5)
oneoff_section.pack(side="left", expand=True, fill="both", padx=5, pady=5)

# --- Add income form inside Income Section ---
setup_income_form(income_section)

# --- Add expense form inside Recurring Section ---
setup_recurring_form(recurring_section)

# --- Add expense form inside One-Off Section ---
setup_oneoff_form(oneoff_section)


# --- Dropdown callback ---
def option_changed(choice):
    if choice == "Overview":
        show_frame(overview_frame)
        display_overview_chart(overview_frame)  # Refresh chart!
    elif choice == "List":
        show_frame(list_frame)
        display_list_data(list_frame)
    elif choice == "Add Information":
        show_frame(add_info_frame)


# --- Dropdown setup ---
options = ["Overview", "List", "Add Information"]
selected_option = ctk.StringVar(value=options[0])

option_menu = ctk.CTkOptionMenu(
    app,
    values=options,
    command=option_changed,
    variable=selected_option
)
option_menu.place(relx=0.5, rely=0.07, anchor="center")


# --- Show default frame ---
show_frame(overview_frame)


# --- Run app ---
app.mainloop()
