"""
Help Window
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class ReadmeWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.markdown_viewer = QTextEdit(readOnly=True)
        layout = QVBoxLayout()
        str = ''
        with open('bookkeeper/view/help.md', mode='r', encoding='utf-8') as readme:
            str = readme.read()
        self.markdown_viewer.setMarkdown(str)
        layout.addWidget(self.markdown_viewer)
        self.setLayout(layout)