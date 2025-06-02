import sys
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel,
                               QPushButton, QWidget, QVBoxLayout,
                               QHBoxLayout, QDialog, QLineEdit, QFormLayout)
from PySide6.QtCore import Qt
import database


class IncomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Income")
        layout = QFormLayout()
        self.source_input = QLineEdit()
        self.amount_input = QLineEdit()
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit)
        layout.addRow("Source:", self.source_input)
        layout.addRow("Amount:", self.amount_input)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def submit(self):
        source = self.source_input.text()
        amount = float(self.amount_input.text())
        date = datetime.now().strftime("%Y-%m-%d")
        database.add_income(source, amount, date)
        self.accept()


class ExpenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Expense")
        layout = QFormLayout()
        self.name_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.category_input = QLineEdit()
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Category ID:", self.category_input)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def submit(self):
        name = self.name_input.text()
        amount = float(self.amount_input.text())
        category = int(self.category_input.text())
        date = datetime.now().strftime("%Y-%m-%d")
        database.add_daily_expense(name, amount, category, date)
        self.accept()


class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.resize(900, 600)
        self.current_view = "Chart"
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        vbox = QVBoxLayout()
        title = QLabel("Welcome to your Finance Tracker!")
        title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(title)

        menu_btn = QPushButton("≡")
        menu_btn.clicked.connect(self.open_menu)
        menu_btn.setFixedWidth(40)
        vbox.addWidget(menu_btn, alignment=Qt.AlignRight)

        self.center_label = QLabel(f"View: {self.current_view}")
        self.center_label.setAlignment(Qt.AlignCenter)
        self.center_label.setFixedHeight(300)
        vbox.addWidget(self.center_label)

        hbox = QHBoxLayout()
        left_btn = QPushButton("←")
        left_btn.clicked.connect(self.toggle_view)
        right_btn = QPushButton("→")
        right_btn.clicked.connect(self.toggle_view)
        hbox.addWidget(left_btn)
        hbox.addWidget(right_btn)
        vbox.addLayout(hbox)

        central.setLayout(vbox)
        self.setCentralWidget(central)

    def toggle_view(self):
        self.current_view = (
            "List" if self.current_view == "Chart" else "Chart"
        )
        self.center_label.setText(f"View: {self.current_view}")

    def open_menu(self):
        menu = QDialog(self)
        menu.setWindowTitle("Menu")
        layout = QVBoxLayout()
        income_btn = QPushButton("Add Income")
        income_btn.clicked.connect(self.open_income_dialog)
        expense_btn = QPushButton("Add Expense")
        expense_btn.clicked.connect(self.open_expense_dialog)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(menu.accept)
        layout.addWidget(income_btn)
        layout.addWidget(expense_btn)
        layout.addWidget(close_btn)
        menu.setLayout(layout)
        menu.exec()

    def open_income_dialog(self):
        dlg = IncomeDialog(self)
        dlg.exec()

    def open_expense_dialog(self):
        dlg = ExpenseDialog(self)
        dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec())
