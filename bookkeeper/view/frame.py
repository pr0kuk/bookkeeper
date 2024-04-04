"""
Main Window
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow
from .expenses_widget import ExpenseWidget
from .budget_widget import BudgetWidget
from .category_widget import CategoryWidget
class Frame(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bookkeeper")
        category = CategoryWidget()
        expense = ExpenseWidget(category)
        budget = BudgetWidget(expense.presenter)
        category.category_changed.connect(expense.update_categories)
        expense.expense_changed.connect(budget.retrieve_expense)
        layout = QVBoxLayout()
        for w in [expense, budget]:
            layout.addWidget(w)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)