from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import timetable_calendar
from PyQt6.QtGui import *
import section_calendar
from widgets import *
from typing import *
import profiles
from copy import copy


_parent_layout: QLayout
_style: QStyle


def _clear_layout(layout: QLayout) -> None:
    for _ in range(layout.count()):
        layout.takeAt(0).widget().deleteLater()


def initialize(parent_layout: QVBoxLayout, application_style: QStyle) -> None:
    global _parent_layout, _style

    _parent_layout = parent_layout
    _style = application_style


def _delete_profile(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    profiles.remove(profile)
    section_calendar.update()


def _select_profile(date: QDate, profile_id: int) -> None:
    timetable_calendar.set_profile(date, profile_id)
    section_calendar.update()


def _create_profile(date: QDate) -> None:
    profile_id = profiles.add_profile(
        'Безымянный профиль', 
        QColor.fromString('#3F3F3F'),
        { QTime(7, 0, 0, 0): 'melody.wav' }
    )
    timetable_calendar.set_profile(date, profile_id)
    section_calendar.update()


def _create_profile_entry_widget(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]], date: QDate) -> QWidget:
    global _style

    widget = HighlightableWidget(profile['name'])
    widget: QPushButton
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
        _parent_layout.addWidget(Spacer())

        label = QLabel("Профилей не найдено")
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        _parent_layout.addWidget(label)
        _parent_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        icon = _style.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)
        text = "Создать профиль"
        button = QPushButton(icon, text)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        button.clicked.connect(lambda: _create_profile(date))
        _parent_layout.addWidget(button)
        _parent_layout.setAlignment(button, Qt.AlignmentFlag.AlignCenter)

        _parent_layout.addWidget(Spacer())
    else:
        _parent_layout.setContentsMargins(0, 0, 0, 0)
        _parent_layout.setSpacing(0)

        _parent_layout.addWidget(Header('**Выберите профиль**'))

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)

        for profile in profiles.get_all():
            list_layout.addWidget(_create_profile_entry_widget(profile, date))
        
        list_layout.addWidget(Spacer())

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


def _create_profile_info_widget(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> QWidget:
    pass


def _on_edit_melody_name(
    time: QTime, 
    profile_id: int,
    line_edit: DisconnectableLineEdit
 ) -> None:
    profile = profiles.get(profile_id)
    old_profile = profile.copy()
    profile['timetable'][time] = line_edit.text()
    profiles.replace(old_profile, profile)


def _on_edit_time(
    time: QTime, 
    profile_id: int,
    time_edit: DisconnectableTimeEdit,
    melody_edit: DisconnectableLineEdit
) -> None:
    profile = profiles.get(profile_id)
    old_profile = profile.copy()

    new_time = time_edit.time()
    profile['timetable'][new_time] = profile['timetable'][time]
    del(profile['timetable'][time])

    profiles.replace(old_profile, profile)

    time_edit.disconnect_on_time_changed()
    time_edit.connect_on_time_changed(lambda: _on_edit_time(new_time, profile_id, time_edit, melody_edit))
    
    melody_edit.disconnect_on_text_changed()
    melody_edit.connect_on_text_changed(lambda: _on_edit_melody_name(new_time, profile_id, melody_edit))


def _delete_alarm(widget: QWidget, profile_id: int, time: QTime) -> None:
    profile = profiles.get(profile_id)
    new_profile = copy(profile)
    del(new_profile['timetable'][time])
    profiles.replace(profile, new_profile)
    widget.setParent(None)


def _pick_alarm_melody(line_edit: DisconnectableLineEdit) -> None:
    file_name = QFileDialog.getOpenFileName(caption='Выберите мелодию звонка', filter='*.wav')[0]

    if file_name == '':
        return
    
    line_edit.setText(file_name)


def _create_timetable_entry_widget(
    time: QTime, 
    melody_name: str, 
    profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]
) -> QWidget:
    global _style

    widget = HighlightableWidget()

    layout = QGridLayout(widget)

    melody_edit = DisconnectableLineEdit(melody_name)
    melody_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    melody_edit.connect_on_text_changed(lambda: _on_edit_melody_name(time, profile['id'], melody_edit))

    time_edit = DisconnectableTimeEdit(time)
    time_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    time_edit.connect_on_time_changed(lambda: _on_edit_time(time, profile['id'], time_edit, melody_edit))

    layout.addWidget(time_edit, 0, 0)
    layout.addWidget(melody_edit, 1, 0)

    delete_alarm_button = QPushButton()
    delete_alarm_button.setIcon(_style.standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
    delete_alarm_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    delete_alarm_button.clicked.connect(lambda: _delete_alarm(widget, profile['id'], time))
    layout.addWidget(delete_alarm_button, 0, 1)

    pick_melody_button = QPushButton()
    pick_melody_button.setIcon(_style.standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
    pick_melody_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    pick_melody_button.clicked.connect(lambda: _pick_alarm_melody(melody_edit))
    layout.addWidget(pick_melody_button, 1, 1)

    return widget


def _add_alarm(profile_id: int, layout: QLayout) -> None:
    old_profile = profiles.get(profile_id)

    keys = list(old_profile['timetable'].keys())
    if len(keys) == 0:
        last_alarm = QTime(6, 59)
        melody_name = 'melody.wav'
    else:
        last_alarm = keys[-1]
        melody_name = old_profile['timetable'][last_alarm]
    
    last_alarm = last_alarm.addSecs(60)
    
    new_profile = copy(old_profile)
    new_profile['timetable'][last_alarm] = melody_name
    profiles.replace(old_profile, new_profile)

    layout.addWidget(_create_timetable_entry_widget(last_alarm, melody_name, new_profile))


def _create_timetable_widget(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> QWidget:
    widget = SectionFrame()

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(Header('**Расписание**', profile['color']))

    list_widget = QWidget()
    list_layout = QVBoxLayout(list_widget)
    list_layout.setSpacing(0)
    list_layout.setContentsMargins(0, 0, 0, 0)

    for time, melody_name in profile['timetable'].items():
        list_layout.addWidget(_create_timetable_entry_widget(time, melody_name, profile))
    
    layout.addWidget(list_widget)

    bottom_section = QWidget()
    bottom_layout = QVBoxLayout(bottom_section)
    text = "Добавить звонок"
    icon = _style.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)
    add_alarm_button = QPushButton(icon, text)
    add_alarm_button.clicked.connect(lambda: _add_alarm(profile['id'], list_layout))
    bottom_layout.addWidget(add_alarm_button)

    layout.addWidget(bottom_section)

    return widget


def _reflect_profile(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    global _parent_layout

    _parent_layout.setContentsMargins(0, 0, 0, 0)
    _parent_layout.setSpacing(0)

    _parent_layout.addWidget(Header('**Настройка профиля**'))

    list_widget = QWidget()
    list_layout = QVBoxLayout(list_widget)
    list_layout.addWidget(_create_profile_info_widget(profile))
    list_layout.addWidget(_create_timetable_widget(profile))
    list_layout.addWidget(Spacer())

    scroll_area = VerticalScrollArea()
    scroll_area.setWidget(list_widget)
    scroll_area.setWidgetResizable(True)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    _parent_layout.addWidget(scroll_area)


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
