from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
import sys

app = QApplication(sys.argv)
window = QWidget()

def main_window() -> None:
        global window
        layout = QHBoxLayout()
        
        header = QVBoxLayout()
        label = QLabel()
        label.setPixmap(QPixmap('resources/icon.png'))
        header.addWidget(label)
        
        header_text = 
        
        layout.addLayout(header)
        
        window.setLayout(layout)

if __name__ == '__main__':
        window.resize(800, 600)
        rectangle = window.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center)
        window.move(rectangle.topLeft())
        window.show()
        window.setWindowTitle('Звонилка')
        window.setWindowIcon(QIcon('resources/icon.png'))
        main_window()
        sys.exit(app.exec_())
