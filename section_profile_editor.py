from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import profiles
from typing import *
from PyQt6.QtGui import *
from widgets import *
import timetable_calendar as calendar


_parent_layout: QLayout
_style: QStyle


def _clear_layout(layout: QLayout) -> None:
    for _ in range(layout.count()):
        layout.takeAt(0).widget().deleteLater()


def initialize(parent_layout: QVBoxLayout, application_style: QStyle) -> None:
    global _parent_layout, _style

    _parent_layout = parent_layout
    _style = application_style


def create_profile(date: QDate) -> None:
    pass


def create_profile_entry(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]], date: QDate) -> QWidget:
    widget = QWidget()

    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    indicator = QWidget()
    indicator.setAutoFillBackground(True)
    palette = indicator.palette()
    palette.setColor(indicator.backgroundRole(), profile['color'])
    indicator.setPalette(palette)
    indicator.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
    indicator.setFixedWidth(2)
    layout.addWidget(indicator)

    label = QLabel(profile['name'])
    layout.addWidget(label)

    return widget


def no_profile(date: QDate) -> None:
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
        button.clicked.connect(create_profile)
        _parent_layout.addWidget(button)
        _parent_layout.setAlignment(button, Qt.AlignmentFlag.AlignCenter)

        _parent_layout.addWidget(create_spacer())
    else:
        for profile in profiles.get_all():
            _parent_layout.addWidget(create_profile_entry(profile, date))

            divider = QWidget()
            divider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            divider.setFixedHeight(1)
            divider.setAutoFillBackground(True)
            palette = divider.palette()
            palette.setColor(divider.backgroundRole(), _style.standardPalette().text().color())
            divider.setPalette(palette)
            _parent_layout.addWidget(divider)
        
        _parent_layout.addWidget(create_spacer())



def reflect_profile(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    pass


def update(profile_id: int, date: QDate) -> None:
    global _parent_layout

    _clear_layout(_parent_layout)

    if profile_id is not None:
        profile = profiles.get(profile_id)
    else:
        profile = None
    
    if profile is not None:
        reflect_profile(profile)
    else:
        no_profile(date)
