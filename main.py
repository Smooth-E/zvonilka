from email import header
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

app = QApplication(sys.argv)
window = QWidget()

def main_layout() -> None:
        global window
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        header_widget = QWidget()
        header_widget.setObjectName('HeaderWidget')
        stylesheet = 'QWidget#HeaderWidget {background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 transparent, stop:1 yellow); }'
        header_widget.setStyleSheet(stylesheet)
        main_layout.addWidget(header_widget)
        header_layout = QHBoxLayout(header_widget)
        pixmap = QPixmap('resources/icon.png').scaled(70, 70)
        header_icon = QLabel()
        header_icon.setPixmap(pixmap)
        header_icon.setFixedWidth(pixmap.width())
        header_layout.addWidget(header_icon)
        header_text_group_widget = QWidget()
        header_layout.addWidget(header_text_group_widget)
        header_text_group_layout = QVBoxLayout(header_text_group_widget)
        header_main_text = QLabel(text='Звонилка')
        font = header_main_text.font()
        font.setPointSize(14)
        header_main_text.setFont(font)
        header_secondary_text = QLabel(text='Приложение для управления электронными звонками.')
        header_text_group_layout.addWidget(header_main_text)
        header_text_group_layout.addWidget(header_secondary_text)
        
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
        main_layout()
        sys.exit(app.exec_())
