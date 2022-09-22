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
    
    default_melody_widget = QFrame()
    default_melody_widget.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
    useful_part_layout.addWidget(default_melody_widget)
    default_melody_layout = QVBoxLayout(default_melody_widget)
    default_melody_header = QLabel(text='Мелодия звонка по умолчанию: ')
    default_melody_layout.addWidget(default_melody_header)
    default_melody_picker_widget = QWidget()
    default_melody_layout.addWidget(default_melody_picker_widget)
    default_melody_picker_layout = QHBoxLayout(default_melody_picker_widget)
    default_melody_picker_layout.setContentsMargins(0, 0, 0, 0)
    default_melody_picker_display = QLineEdit('some/path/to/something')
    default_melody_picker_layout.addWidget(default_melody_picker_display)
    default_melody_picker_button = QPushButton()
    default_melody_picker_button.setText('Открыть файл')
    pixmap = window.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton)
    default_melody_picker_button.setIcon(pixmap)
    default_melody_picker_layout.addWidget(default_melody_picker_button)
    
    two_columns_widget = QWidget()
    two_columns_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
    two_columns_layout = QHBoxLayout(two_columns_widget)
    two_columns_layout.setContentsMargins(0, 0, 0, 0)
    
    timetable_widget = QFrame()
    timetable_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    timetable_widget.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
    two_columns_layout.addWidget(timetable_widget)
    timetable_layout = QVBoxLayout(timetable_widget)
    timetable_header_widget = QWidget()
    timetable_layout.addWidget(timetable_header_widget)
    timetable_header_layout = QHBoxLayout(timetable_header_widget)
    timetable_header_layout.setContentsMargins(0, 0, 0, 0)
    timetable_header_label = QLabel('Расписание звонков')
    timetable_header_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    timetable_header_layout.addWidget(timetable_header_label)
    timetable_header_button = QPushButton()
    timetable_header_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    timetable_header_button.setIcon(window.style().standardIcon(QStyle.StandardPixmap.SP_FileLinkIcon))
    timetable_header_layout.addWidget(timetable_header_button)
    
    timetable_frame = QFrame()
    timetable_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
    timetable_frame.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
    timetable_layout.addWidget(timetable_frame)
    timetable_list_layout = QVBoxLayout(timetable_frame)
    
    timetable_play_now_button = QPushButton('[Alt + Enter] Сыграть звонок сейчас')
    timetable_play_now_button.setIcon(window.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
    timetable_play_now_button.setShortcut('Alt + Enter')
    timetable_layout.addWidget(timetable_play_now_button)
    
    extra_widget = QFrame()
    extra_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    extra_widget.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
    two_columns_layout.addWidget(extra_widget)
    extra_layout = QVBoxLayout(extra_widget)
    extra_header_widget = QWidget()
    extra_layout.addWidget(extra_header_widget)
    extra_header_layout = QHBoxLayout(extra_header_widget)
    extra_header_layout.setContentsMargins(0, 0, 0, 0)
    extra_header_label = QLabel('Доплнителные кнопки')
    extra_header_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    extra_header_layout.addWidget(extra_header_label)
    extra_header_button = QPushButton()
    extra_header_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    extra_header_button.setIcon(window.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
    extra_header_layout.addWidget(extra_header_button)
    
    extra_buttons_widget = QFrame()
    extra_buttons_widget.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
    extra_buttons_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
    extra_layout.addWidget(extra_buttons_widget)
    extra_buttons_layout = QVBoxLayout(extra_buttons_widget)
    for index in range(1, 11, 1):
        if index == 10: number = 0
        else: number = index
        button = QPushButton('[Alt + ' + str(number) + '] Какой-то текст')
        button.setIcon(window.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
        button.setShortcut('Alt + ' + str(number))
        extra_buttons_layout.addWidget(button)
    
    useful_part_layout.addWidget(two_columns_widget)
    
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
