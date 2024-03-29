import timetable_calendar as calendar
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from copy import copy
from typing import *
import random
import json
import os


"""
Формат хранения профилей в файле JSON:

[
    {
        "id": 123,
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
        "id": 123,
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


_file_path = 'profiles.json'
_profiles_loaded = False
_profiles: List[Dict[str, Union[str, QColor, Dict[QTime, str]]]]


def _is_unique_id(id: int) -> bool:
    global _profiles

    for profile in _profiles:
        if profile['id'] == id:
            return False
    return True


def _generate_unique_id() -> int:
    id = random.randint(0, 1001)
    while True:
        if _is_unique_id(id):
            return id
        id = random.randint(0, 1001)


def _deserialize_timetable(timetable: Dict[str, str]) -> Dict[QTime, str]:
    new_timetable = { }

    for key, value in timetable.items():
        key_parts = [int(x) for x in key.split(':')]
        new_key = QTime(key_parts[0], key_parts[1], 0)
        new_timetable[new_key] = value
    
    return new_timetable


def _serialize_timetable(timetable: Dict[QTime, str]) -> Dict[str, str]:
    new_timetable = { }

    for key, value in timetable.items():
        new_key = f'{key.hour():02d}:{key.minute():02d}'
        new_timetable[new_key] = value

    return new_timetable


def _load_profiles() -> None:
    global _file_path, _profiles, _profiles_loaded

    if _profiles_loaded:
        return
    
    _profiles = []
    _profiles_loaded = True

    if not os.path.exists(_file_path):
        return
    
    try:
        file = open(_file_path, 'r', encoding='utf-8')
        loaded_profiles = json.load(file)
        file.close()
    except Exception as exception:
        print('Ошибка загрузки файла профилей!')
        print(exception.with_traceback(None))
        return
    
    # Конвертация из формата хранения в формат объект
    _profiles = []
    for profile in loaded_profiles:
        new_profile = { }
        new_profile['id'] = int(profile['id'])
        new_profile['name'] = str(profile['name'])
        new_profile['color'] = QColor(int(profile['color']))
        new_profile['timetable'] = _deserialize_timetable(profile['timetable'])
        _profiles.append(new_profile)


def _save_profiles() -> None:
    global _file_path, _profiles

    serialized_profiles = []
    for profile in _profiles:
        serialized = {  }
        serialized['id'] = profile['id']
        serialized['name'] = profile['name']
        serialized['color'] = profile['color'].rgb()
        serialized['timetable'] = _serialize_timetable(profile['timetable'])
        serialized_profiles.append(serialized)

    try:
        file = open(_file_path, 'w+', encoding='utf-8')
        json.dump(serialized_profiles, file, ensure_ascii=False, sort_keys=True, indent=4)
        file.close()
        print('Профили успешно сохранены!')
        # print(json.dumps(serialized_profiles, ensure_ascii=False, sort_keys=True,  indent=4))
    except Exception as exception:
        print('Ошибка сохранения профилей!')
        print(exception.with_traceback(None))


def add_profile(name: str, color: QColor, timetable: Dict[QTime, str]) -> int:
    global _profiles
    _load_profiles()

    color.setAlpha(255)
    profile_id = _generate_unique_id()
    profile = {
        'id': profile_id,
        'name': name,
        'color': color,
        'timetable': timetable
    }
    _profiles.append(profile)

    _save_profiles()

    return profile_id


def get_all() -> List[Dict[str, Union[str, QColor, Dict[QTime, str]]]]:
    global _profiles
    _load_profiles()
    return copy(_profiles)


def get(profile_id: int) -> Union[Dict[str, Union[str, QColor, Dict[QTime, str]]], None]:
    global _profiles
    _load_profiles()

    for profile in _profiles:
        if profile['id'] == profile_id:
            return copy(profile)
    return None


def replace(
    value_from: Dict[str, Union[str, QColor, Dict[QTime, str]]], 
    value_to: Dict[str, Union[str, QColor, Dict[QTime, str]]]
) -> None:
    global _profiles
    _load_profiles()

    index = _profiles.index(value_from)
    _profiles[index] = value_to
    _save_profiles()


def remove(profile: Dict[str, Union[str, QColor, Dict[QTime, str]]]) -> None:
    global _profiles
    _load_profiles()

    _profiles.remove(profile)
    _save_profiles()

    calendar.notify_profile_removal(profile['id'])
