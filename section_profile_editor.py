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


def _show_profile_deletion_warning(widget: QWidget, profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    icon = _style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
    title = 'Удаление профиля'
    text = \
        'Внимание! ' + \
        'Удаление профиля также отвяжет его от всех дней, на которые он был присвоен. ' + \
        'Вы уверены, что хотите удалить профиль, а отвязать его от всех соответствующих дней?'

    message_box = QMessageBox(QMessageBox.Icon.Warning, title, text, QMessageBox.Yes | QMessageBox.No, widget)
    button_yes = message_box.button(QMessageBox.Yes)
    button_yes.setText('Да')
    button_no = message_box.button(QMessageBox.No)
    button_no.setText('Нет')
    message_box.setDefaultButton(button_no)
    message_box.exec()

    if message_box.clickedButton() == button_yes:
        _delete_profile(profile)


def _delete_profile(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    profiles.remove(profile)
    section_calendar.update()


def _select_profile(date: QDate, profile_id: int) -> None:
    timetable_calendar.set_profile(date, profile_id)
    section_calendar.update()


def _create_profile(date: QDate) -> None:
    profile_id = profiles.add_profile(
        'Безымянный профиль',
        QColor('#3F3F3F'),
        {QTime(7, 0, 0, 0): 'melody.wav'}
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
    button_delete.clicked.connect(lambda: _show_profile_deletion_warning(widget, profile))
    layout.addWidget(button_delete)

    return widget


def _reflect_no_profile(date: QDate) -> None:
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


def _on_profile_color_selected(profile_id: int, color_dialog: QColorDialog) -> None:
    profile = profiles.get(profile_id)
    old_profile = copy(profile)
    profile['color'] = color_dialog.selectedColor()
    profiles.replace(old_profile, profile)
    section_calendar.update()


def _pick_profile_color(profile_id: int) -> None:
    profile = profiles.get(profile_id)
    dialog = QColorDialog(profile['color'])
    dialog.colorSelected.connect(lambda: _on_profile_color_selected(profile_id, dialog))
    dialog.show()


def _on_profile_name_changed(profile_id: int, line_edit: QLineEdit) -> None:
    profile = profiles.get(profile_id)
    old_profile = copy(profile)
    profile['name'] = line_edit.text()
    profiles.replace(old_profile, profile)


def _on_clear_profile(date: QDate) -> None:
    timetable_calendar.clear_profile(date)
    section_calendar.update()


def _create_profile_info_widget(date: QDate, profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> QWidget:
    widget = SectionFrame()

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    layout.addWidget(Header('**Свойства профиля**', profile['color']))

    options_widget = QWidget()
    options_layout = QGridLayout(options_widget)

    description_profile_name = QLabel(text='Имя:')
    description_profile_name.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
    options_layout.addWidget(description_profile_name, 0, 0)

    profile_name_edit = QLineEdit(profile['name'])
    profile_name_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    profile_name_edit.textChanged.connect(lambda: _on_profile_name_changed(profile['id'], profile_name_edit))
    options_layout.addWidget(profile_name_edit, 0, 1)

    description_profile_color = QLabel(text='Цвет:')
    description_profile_color.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
    options_layout.addWidget(description_profile_color, 1, 0)

    change_color_button = QPushButton('something')
    change_color_button.clicked.connect(lambda: _pick_profile_color(profile['id']))

    change_color_helper_layout = QHBoxLayout(change_color_button)
    change_color_helper_layout.setContentsMargins(4, 4, 4, 4)

    color_name = profile['color'].name()

    color_swatch = QWidget()
    color_swatch.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    color_swatch.setAutoFillBackground(True)
    color_swatch.setStyleSheet(f'background-color: {color_name}')

    change_color_helper_layout.addWidget(color_swatch)
    options_layout.addWidget(change_color_button, 1, 1)

    layout.addWidget(options_widget)

    icon = _style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
    clear_profile_button = QPushButton(icon, 'Сменить профиль')
    clear_profile_button.clicked.connect(lambda: _on_clear_profile(date))
    clear_profile_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    options_layout.addWidget(clear_profile_button, 2, 0, 1, 2)

    return widget


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
        time_line_edit: CachingDisconnectableLineEdit,
        melody_edit: DisconnectableLineEdit
) -> None:
    profile = profiles.get(profile_id)
    old_profile = profile.copy()

    split_up_text = time_line_edit.text().split(':')

    correct_formatting = \
        len(split_up_text) == 2 and \
        split_up_text[0].isdigit() and \
        split_up_text[1].isdigit() and \
        0 <= int(split_up_text[0]) <= 23 and \
        0 <= int(split_up_text[1]) <= 59

    if not correct_formatting:
        print("Неверное форматирование времени!")
        time_line_edit.set_icon(_style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical))
        return

    new_time = QTime(int(split_up_text[0]), int(split_up_text[1]), 0)
    if (time != new_time and profile['timetable'].get(new_time) is not None):
        print('Звонок на это время уже существует!')
        time_line_edit.set_icon(_style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning))
        return

    if time == new_time:
        print('Новое введенное время идентично предыдущему!')
        time_line_edit.set_icon(None)
        return

    profile['timetable'][new_time] = profile['timetable'][time]
    del(profile['timetable'][time])

    profiles.replace(old_profile, profile)

    time_line_edit.disconnect_on_text_changed()
    time_line_edit.connect_on_text_changed(lambda: _on_edit_time(new_time, profile_id, time_line_edit, melody_edit))

    melody_edit.disconnect_on_text_changed()
    melody_edit.connect_on_text_changed(lambda: _on_edit_melody_name(new_time, profile_id, melody_edit))

    time_line_edit.set_icon(_style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), True)
    time_line_edit.apply_changes()


def _delete_alarm(widget: QWidget, profile_id: int, time: QTime) -> None:
    profile = profiles.get(profile_id)
    new_profile = copy(profile)
    del (new_profile['timetable'][time])
    profiles.replace(profile, new_profile)
    widget.setParent(None)


def _pick_alarm_melody(line_edit: DisconnectableLineEdit) -> None:
    file_name = QFileDialog.getOpenFileName(caption='Выберите мелодию звонка', filter='*.wav')[0]

    if file_name == '':
        return

    line_edit.setText(file_name)


def _create_profile_timetable_entry_widget(
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

    time_line_edit = CachingDisconnectableLineEdit(f'{time.hour():02d}:{time.minute():02d}')
    time_line_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    time_line_edit.connect_on_text_changed(lambda: _on_edit_time(time, profile['id'], time_line_edit, melody_edit))

    layout.addWidget(time_line_edit, 0, 0)
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

    layout.addWidget(_create_profile_timetable_entry_widget(last_alarm, melody_name, new_profile))


def _create_profile_timetable_widget(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> QWidget:
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
        list_layout.addWidget(_create_profile_timetable_entry_widget(time, melody_name, profile))

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


def _reflect_profile(date: QDate, profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    global _parent_layout

    _parent_layout.setContentsMargins(0, 0, 0, 0)
    _parent_layout.setSpacing(0)

    _parent_layout.addWidget(Header('**Настройка профиля**'))

    list_widget = QWidget()
    list_layout = QVBoxLayout(list_widget)
    list_layout.addWidget(_create_profile_info_widget(date, profile))
    list_layout.addWidget(_create_profile_timetable_widget(profile))
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
        _reflect_profile(date, profile)
    else:
        _reflect_no_profile(date)
