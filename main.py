import section_profile_editor
import section_play_melody
import section_calendar
from widgets import *
import settings
import notifier
import sys


def create_settings_widget() -> QWidget:
    frame = SectionFrame()
    QVBoxLayout(frame)
    return frame


def create_timetable_widget() -> QWidget:
    global style

    frame = SectionFrame()
    layout = QVBoxLayout(frame)

    section_profile_editor.initialize(layout, style)
    
    return frame


def create_base_layout() -> QHBoxLayout:
    global style

    timetable_widget = create_timetable_widget()
    calendar_section = section_calendar.create()
    settings_section = create_settings_widget()
    immediate_section = section_play_melody.create(style)

    bottom_layout = QHBoxLayout()
    bottom_layout.addWidget(immediate_section, 1)
    bottom_layout.addWidget(settings_section, 1)

    left_section = QVBoxLayout()
    left_section.addWidget(calendar_section)
    left_section.addLayout(bottom_layout)

    base_layout = QHBoxLayout()
    base_layout.addLayout(left_section, 2)
    base_layout.addWidget(timetable_widget, 1)

    return base_layout


def initialize_app() -> None:
    global application, window, style

    application = QApplication(sys.argv)
    window = QWidget()
    style = window.style()

    settings.load_settings()

    base_layout = create_base_layout()
    window.setLayout(base_layout)

    window.resize(1920 // 2, 1080 // 2)

    rectangle = window.frameGeometry()
    center = application.primaryScreen().availableGeometry().center()
    rectangle.moveCenter(center)
    window.move(rectangle.topLeft())

    window.show()
    window.setWindowTitle('Звонилка')
    window.setWindowIcon(QIcon('icon.png'))

    notifier.restart()
    application.exec()
    notifier.stop()


if __name__ == '__main__':
    sys.exit(initialize_app())
