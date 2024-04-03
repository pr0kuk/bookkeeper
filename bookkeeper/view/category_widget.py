"""
Edit Widget
"""
from PySide6 import QtWidgets
from .edit_window import EditCtgWindow

def set_data(box: QtWidgets.QComboBox, cats: list[str]) -> None:
    for cat in cats:
        box.addItem(cat)

class EditWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Редактирование"))
        cat_edit_button = QtWidgets.QPushButton("Редактировать")
        cat_box = QtWidgets.QComboBox()
        labels = [QtWidgets.QLabel("Сумма"),QtWidgets.QLineEdit("0"), QtWidgets.QLabel(), QtWidgets.QLabel("Категория"), cat_box, cat_edit_button, QtWidgets.QLabel(),QtWidgets.QPushButton("Добавить"), QtWidgets.QLabel()]
        glayout = QtWidgets.QGridLayout()
        for i, label in zip(range(len(labels)), labels):
            print(i, i//3, i%3)
            glayout.addWidget(label, i//3, i%3)
        gwidget = QtWidgets.QWidget()
        gwidget.setLayout(glayout)
        layout.addWidget(gwidget)
        self.cat_list = ["Продукты", "Книги"]
        set_data(cat_box, self.cat_list)
        cat_edit_button.clicked.connect(self.open_window)
        self.setLayout(layout)

    def open_window(self):
        self.edit_ctg = EditCtgWindow(self.cat_list)
        self.edit_ctg.show()