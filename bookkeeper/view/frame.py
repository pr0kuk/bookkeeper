"""
Main Window
"""
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QToolBar
from bookkeeper.view.expenses.expenses_widget import ExpenseWidget
from bookkeeper.view.budget.budget_widget import BudgetWidget
from bookkeeper.view.category.category_widget import CategoryWidget
from bookkeeper.view.help_window import ReadmeWindow


class Frame(QMainWindow):
    """
    Главное окно
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bookkeeper")
        category = CategoryWidget()
        expense = ExpenseWidget(category)
        budget = BudgetWidget(expense.presenter)
        category.category_changed.connect(expense.update_categories)
        expense.expense_changed.connect(budget.retrieve_expense)
        toolbar = QToolBar("toolbar")
        self.addToolBar(toolbar)
        button_action = QAction("Help", self)
        button_action.setStatusTip("Readme")
        self.help_window = ReadmeWindow()
        button_action.triggered.connect(self.open_help)
        toolbar.addAction(button_action)
        layout = QVBoxLayout()
        for w in [expense, budget]:
            layout.addWidget(w)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_help(self) -> None:
        """
        Открыть окно помощи
        """
        self.help_window.show()
