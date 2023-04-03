from PyQt6.QtCore import *
from copy import copy
from typing import *
import json
import os

_file_path = 'calendar.json'
_loaded = False
_calendar: Dict[QDate, int] = {}


def _save_calendar() -> None:
    global _calendar, _file_path

    serialized_calendar = {}
    for key, value in _calendar.items():
        new_key = f'{key.year()}.{key.month()}.{key.day()}'
        serialized_calendar[new_key] = value

    try:
        file = open(_file_path, 'w+')
        json.dump(serialized_calendar, file, ensure_ascii=False, indent=4, sort_keys=True)
        file.close()
    except Exception as exception:
        print('Ошибка сохранения календаря!')
        print(exception.with_traceback(None))


def _load_calendar() -> None:
    global _loaded, _file_path, _calendar

    if _loaded:
        return

    _calendar = {}
    _loaded = True

    if not os.path.exists(_file_path):
        return

    try:
        file = open(_file_path, 'r', encoding='utf-8')
        raw_calendar = json.load(file)
        file.close()
    except Exception as exception:
        return

    _calendar = {}
    for key, value in raw_calendar.items():
        year, month, day = (int(x) for x in key.split('.'))
        new_key = QDate(year, month, day)
        _calendar[new_key] = value


def set_profile(date: QDate, profile_id: int) -> None:
    global _calendar
    _load_calendar()

    _calendar[date] = profile_id
    _save_calendar()


def notify_profile_removal(profile_id: int) -> None:
    global _calendar
    _load_calendar()

    _calendar = {key: value for key, value in _calendar.items() if value != profile_id}

    _save_calendar()


def get_calendar() -> Dict[QDate, int]:
    global _calendar
    _load_calendar()
    return copy(_calendar)


def get_profile_id(date: QDate) -> Union[int, None]:
    global _calendar
    _load_calendar()
    return _calendar.get(date)


def clear_profile(date: QDate) -> None:
    global _calendar
    _load_calendar()

    print('Got date: ' + str(date))
    _calendar = {key: value for key, value in _calendar.items() if key != date}

    print("saving!")
    _save_calendar()
