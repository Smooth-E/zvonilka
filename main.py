import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDesktopWidget

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.resize(800, 600)
rectangle = window.frameGeometry()
center = QDesktopWidget().availableGeometry().center()
rectangle.moveCenter(center)
window.move(rectangle.topLeft())
window.show()
window.setWindowTitle('Звонилка')
window.setWindowIcon(QtGui.QIcon('resources/icon.png'))
sys.exit(app.exec_())
