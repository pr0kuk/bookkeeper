"""
Help Window
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class ReadmeWindow(QWidget):
    """
    Виджет окна помощи
    """

    def __init__(self) -> None:
        super().__init__()
        self.markdown_viewer = QTextEdit(readOnly=True)
        layout = QVBoxLayout()
        self.mdtext = ''
        with open('bookkeeper/view/help.md', mode='r', encoding='utf-8') as readme:
            self.mdtext = readme.read()
        self.markdown_viewer.setMarkdown(self.mdtext)
        layout.addWidget(self.markdown_viewer)
        self.setLayout(layout)

    def get_mdtext(self) -> str:
        """
        Получить текст помощи в виде строки
        """
        return self.mdtext

    def is_mdtext_empty(self) -> bool:
        """
        Проверить удалось ли прочесть файл
        """
        return self.mdtext == ''
