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
    global _style

    widget = QWidget()

    layout = QHBoxLayout(widget)

    indicator = QWidget()
    indicator.setAutoFillBackground(True)
    palette = indicator.palette()
    palette.setColor(indicator.backgroundRole(), profile['color'])
    indicator.setPalette(palette)
    indicator.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
    indicator.setFixedWidth(2)
    layout.addWidget(indicator)

    label = QLabel(profile['name'])
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
    layout.addWidget(label)

    icon_delete = _style.standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton)
    button_delete = QPushButton(icon=icon_delete)
    layout.addWidget(button_delete)

    icon_use = _style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
    button_use = QPushButton(icon=icon_use)
    layout.addWidget(button_use)

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
        _parent_layout.setContentsMargins(0, 0, 0, 0)
        _parent_layout.setSpacing(0)

        header_text = '**Список профилей**'
        header = QLabel(header_text)
        header.setTextFormat(Qt.TextFormat.MarkdownText)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet('padding: 4')
        header.setAutoFillBackground(True)
        header_palette = header.palette()
        header_palette.setColor(header.backgroundRole(), QApplication.palette().highlight().color())
        header_palette.setColor(header.foregroundRole(), QApplication.palette().highlightedText().color())
        header.setPalette(header_palette)
        _parent_layout.addWidget(header)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)

        scroll_area = VerticalScrollArea()
        scroll_area.setWidget(list_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        _parent_layout.addWidget(scroll_area)

        for profile in profiles.get_all():
            list_layout.addWidget(create_profile_entry(profile, date))
        
        list_layout.addWidget(create_spacer())


def reflect_profile(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
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
        reflect_profile(profile)
    else:
        no_profile(date)
