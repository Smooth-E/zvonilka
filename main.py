from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *
from playsound import playsound as play_sound
import application_settings
import sys
import os
import json


application = QApplication(sys.argv)
window = QWidget()
style = window.style()

timetable_section: QHBoxLayout = None

calendar_section: QWidget = None

settings_section: QWidget = None

immediate_section: QWidget = None
immediate_melody_line_edit: QLineEdit = None


def create_section_frame() -> QFrame:
    frame = QFrame()
    frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
    return frame


def create_calendar_section() -> QWidget:
    frame = create_section_frame()
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    calendar = QCalendarWidget()
    calendar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(calendar)
    return frame


def on_default_melody_path_edited(new_path: str) -> None:
    application_settings.settings['default_melody'] = new_path
    application_settings.save_settings()


def play_default_melody() -> None:
    melody = application_settings.settings['default_melody']
    play_sound(melody)


def pick_default_melody() -> None:
    global immediate_melody_line_edit

    file_name = QFileDialog.getOpenFileName(caption='Выберите мелодию звонка по умолчанию', filter='*.wav')[0]

    if file_name == '':
        return
    
    application_settings.settings['default_melody'] = file_name
    application_settings.save_settings()
    immediate_melody_line_edit.setText(file_name)


def create_immediate_section() -> QWidget:
    global immediate_melody_line_edit

    frame = create_section_frame()
    layout = QVBoxLayout(frame)
    
    top_bar_layout = QHBoxLayout()

    label = QLabel('Мелодия для проигрывания:')
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    button_pick = QPushButton(icon=style.standardIcon(QStyle.StandardPixmap.SP_FileIcon))
    button_pick.clicked.connect(pick_default_melody)

    top_bar_layout.addWidget(label)
    top_bar_layout.addWidget(button_pick)
    layout.addLayout(top_bar_layout)

    default_melody = application_settings.settings['default_melody']
    immediate_melody_line_edit = QLineEdit(default_melody)
    immediate_melody_line_edit.textEdited.connect(on_default_melody_path_edited)
    layout.addWidget(immediate_melody_line_edit)

    icon = style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
    button_play = QPushButton(icon, 'Воспроизвести мелодию звонка')
    button_play.clicked.connect(play_default_melody)
    layout.addWidget(button_play)

    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(spacer)

    return frame


def create_settings_widget() -> QWidget:
    frame = create_section_frame()
    QVBoxLayout(frame)
    return frame


def create_timetable_widget() -> QWidget:
    frame = create_section_frame()
    QVBoxLayout(frame)
    return frame


def create_base_layout() -> QWidget:
    timetable_section = create_timetable_widget()
    calendar_section = create_calendar_section()
    settings_section = create_settings_widget()
    immediate_section = create_immediate_section()

    bottom_layout = QHBoxLayout()
    bottom_layout.addWidget(immediate_section, 1)
    bottom_layout.addWidget(settings_section, 1)

    left_section = QVBoxLayout()
    left_section.addWidget(calendar_section, 2)
    left_section.addLayout(bottom_layout, 1)

    base_layout = QHBoxLayout()
    base_layout.addLayout(left_section, 2)
    base_layout.addWidget(timetable_section, 1)

    return base_layout


def initialize_app() -> None:
    application_settings.load_settings()

    base_layout = create_base_layout()
    window.setLayout(base_layout)

    window.resize(1920 // 2, 1080 // 2)

    rectangle = window.frameGeometry()
    center = QGuiApplication.primaryScreen().availableGeometry().center()
    rectangle.moveCenter(center)
    window.move(rectangle.topLeft())

    window.show()
    window.setWindowTitle('Звонилка')
    window.setWindowIcon(QIcon('resources/icon.png'))
    sys.exit(application.exec())


if __name__ == '__main__':
    initialize_app()
