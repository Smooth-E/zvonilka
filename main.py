from email import header
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

app = QApplication(sys.argv)
window = QWidget()

def main_window() -> None:
        global window
        main_layout = QVBoxLayout()
        
        header_height = 100
        header_widget = QWidget()
        
        header_layout = QHBoxLayout(header_widget)
        
        header_pixmap = QPixmap('resources/icon.png')
        header_pixmap = header_pixmap.scaled(header_height - 20, header_height - 20, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        
        header_label = QLabel()
        header_label.setPixmap(header_pixmap)
        header_layout.addWidget(header_label)
        
        header_text = QLabel(text='Звонилка')
        header_layout.addWidget(header_text)
        header_widget.setFixedHeight(header_height)
        
        main_layout.addWidget(header_widget)
        main_layout.addStretch(1)
        
        window.setLayout(main_layout)

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
