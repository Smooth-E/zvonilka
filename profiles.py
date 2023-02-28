from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import *
from copy import copy
import json
import os


_file_path = 'profiles.json'
_profiles_loaded = False

"""
profiles = [
    {
        "name": "Name",
        "color": <int color value>
        "timetable": {
            "11:55": "melody.wav",
            "11:55": "melody.wav",
            "11:55": "melody.wav",
            ...
        }
    },
    {
        "name": "Name",
        "color": <int color value>
        "timetable": {
            "11:55": "melody.wav",
            "11:55": "melody.wav",
            "11:55": "melody.wav",
            ...
        }
    },
    ...
]
"""
_profiles: List[Dict[str, Union[str, Dict[str, str]]]]


def _load_profiles() -> None:
    global _file_path, _profiles, _profiles_loaded

    if _profiles_loaded:
        return
    
    _profiles_loaded = True

    if not os.path.exists(_file_path):
        return
    
    try:
        file = open(_file_path, 'r')
        _profiles = json.load(file)
        file.close()
    except Exception:
        pass


def _save_profiles() -> None:
    global _file_path, _profiles

    try:
        file = open(_file_path, 'w+')
        json.dump(_profiles, file)
        file.close()
    except Exception as exception:
        print('Ошибкам сохранения профилей!')
        print(exception.with_traceback())


def add_profile(name: str, color: QColor, timetable: Dict[QTime, str]) -> None:
    global _profiles

    color.setAlpha(255)

    converted_timetable = {}
    for key, value in timetable.items():
        new_key = f'{key.hour}:{key.minute}'
        converted_timetable[new_key] = value

    profile = {
        "name": name,
        "color": color.value(),
        "timetable": converted_timetable
    }

    _profiles.append(profile)
    _save_profiles()