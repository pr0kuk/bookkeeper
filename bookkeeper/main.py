"""
main
"""
import sys
from PySide6.QtWidgets import QApplication
from bookkeeper.view.frame import Frame

app = QApplication(sys.argv)
window = Frame()
window.show()
sys.exit(app.exec())
