import customtkinter as ctk

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


# --- Add labels (just placeholders) ---
ctk.CTkLabel(overview_frame, text="Overview Section").pack(pady=20)
ctk.CTkLabel(list_frame, text="List Section").pack(pady=20)
ctk.CTkLabel(add_info_frame, text="Add Info Section").pack(pady=20)


# --- Dropdown callback ---
def option_changed(choice):
    if choice == "Overview":
        show_frame(overview_frame)
    elif choice == "List":
        show_frame(list_frame)
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

# Show default frame
show_frame(overview_frame)


# --- Run app ---
app.mainloop()
