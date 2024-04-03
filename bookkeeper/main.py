import sys

from PySide6 import QtWidgets
from view.frame import Frame

app = QtWidgets.QApplication(sys.argv)
window = Frame()
window.show()
sys.exit(app.exec())