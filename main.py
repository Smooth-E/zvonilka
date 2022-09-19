from email import header
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import json

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
        
        with open('config.json', 'r') as config:
                config : dict = json.load(config)
        
        useful_part_widget = QWidget()
        main_layout.addWidget(useful_part_widget)
        useful_part_layout = QVBoxLayout(useful_part_widget)
        
        default_melody_widget = QLabel()
        default_melody_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)
        default_melody_widget.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        useful_part_layout.addWidget(default_melody_widget)
        default_melody_layout = QVBoxLayout(default_melody_widget)
        default_melody_header = QLabel(text='Мелодия звонка по умолчанию: ')
        default_melody_layout.addWidget(default_melody_header)
        default_melody_picker_widget = QWidget()
        default_melody_layout.addWidget(default_melody_picker_widget)
        default_melody_picker_layout = QHBoxLayout(default_melody_picker_widget)
        default_melody_picker_layout.setSpacing(0)
        default_melody_picker_display = QTextEdit('some/path/to/something')
        default_melody_picker_layout.addWidget(default_melody_picker_display)
        
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
