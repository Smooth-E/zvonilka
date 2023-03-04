from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import profiles
from typing import *
from PyQt6.QtGui import *
from widgets import *
import section_calendar
import timetable_calendar


_parent_layout: QLayout
_style: QStyle


def _clear_layout(layout: QLayout) -> None:
    for _ in range(layout.count()):
        layout.takeAt(0).widget().deleteLater()


def initialize(parent_layout: QVBoxLayout, application_style: QStyle) -> None:
    global _parent_layout, _style

    _parent_layout = parent_layout
    _style = application_style


def _create_profile(date: QDate) -> None:
    pass


def _delete_profile(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    profiles.remove(profile)
    section_calendar.reselect_date()

def _select_profile(date: QDate, profile_id: int) -> None:
    timetable_calendar.set_profile(date, profile_id)
    section_calendar.reselect_date()


def _create_profile(date: QDate) -> None:
    profile_id = profiles.add_profile(
        'Безымянный профиль', 
        QColor.fromString('#3F3F3F'),
        { QTime(7, 0, 0, 0): 'melody.wav' }
    )
    timetable_calendar.set_profile(date, profile_id)
    section_calendar.reselect_date()


def _create_profile_entry_widget(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]], date: QDate) -> QWidget:
    global _style

    object_name = 'ProfileEntryTopParent'
    highlight_color = QApplication.palette().base().color().name()
    stylesheet = f"""
    QWidget#{object_name}:hover {{ 
        background-color: {highlight_color}; 
    }}
    """

    widget = ClickableQWidget()
    widget.setObjectName(object_name)
    widget.setStyleSheet(stylesheet)
    widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    widget.setClickCallback(lambda: _select_profile(date, profile['id']))

    layout = QHBoxLayout(widget)

    indicator = QWidget()
    indicator.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
    indicator.setFixedWidth(2)
    indicator.setAutoFillBackground(True)
    palette = indicator.palette()
    palette.setColor(indicator.backgroundRole(), profile['color'])
    indicator.setPalette(palette)
    layout.addWidget(indicator)

    label = QLabel(profile['name'])
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
    layout.addWidget(label)

    icon_delete = _style.standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton)
    button_delete = QPushButton(icon=icon_delete)
    button_delete.clicked.connect(lambda: _delete_profile(profile))
    layout.addWidget(button_delete)

    return widget


def _no_profile(date: QDate) -> None:
    global _parent_layout, _style

    all_profiles = profiles.get_all()

    if len(all_profiles) == 0:
        _parent_layout.addWidget(create_spacer())

        label = QLabel("Профилей не найдено")
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        _parent_layout.addWidget(label)
        _parent_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        icon = _style.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)
        text = "Создать профиль"
        button = QPushButton(icon, text)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        button.clicked.connect(_create_profile)
        _parent_layout.addWidget(button)
        _parent_layout.setAlignment(button, Qt.AlignmentFlag.AlignCenter)

        _parent_layout.addWidget(create_spacer())
    else:
        _parent_layout.setContentsMargins(0, 0, 0, 0)
        _parent_layout.setSpacing(0)

        header_text = '**Список профилей**'
        header = QLabel(header_text)
        header.setTextFormat(Qt.TextFormat.MarkdownText)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setContentsMargins(4, 4, 4, 4)
        header.setAutoFillBackground(True)
        header_palette = header.palette()
        header_palette.setColor(header.backgroundRole(), QApplication.palette().highlight().color())
        header_palette.setColor(header.foregroundRole(), QApplication.palette().highlightedText().color())
        header.setPalette(header_palette)
        _parent_layout.addWidget(header)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)

        for profile in profiles.get_all():
            list_layout.addWidget(_create_profile_entry_widget(profile, date))
        
        list_layout.addWidget(create_spacer())

        scroll_area = VerticalScrollArea()
        scroll_area.setWidget(list_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        _parent_layout.addWidget(scroll_area)

        helper_widget = QWidget()
        helper_layout = QVBoxLayout(helper_widget)
        icon = _style.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)
        text = 'Создать новый профиль'
        button_create_profile = QPushButton(icon=icon, text=text)
        button_create_profile.clicked.connect(lambda: _create_profile(date))
        helper_layout.addWidget(button_create_profile)
        _parent_layout.addWidget(helper_widget)


def _reflect_profile(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    pass


def update(profile_id: int, date: QDate) -> None:
    global _parent_layout

    _clear_layout(_parent_layout)
    _parent_layout.setContentsMargins(-1, -1, -1, -1)

    if profile_id is not None:
        profile = profiles.get(profile_id)
    else:
        profile = None
    
    if profile is not None:
        _reflect_profile(profile)
    else:
        _no_profile(date)
