import os
import json


_file_path = 'settings.json'
_default_settings_data = {
    'default_melody': 'melody.wav'
}

settings: dict


def _load_settings_from_file() -> None:
    global settings

    try:
        file = open(_file_path, 'r')
        data = file.read()
        settings = json.loads(data)
        file.close()
    except Exception as exception:
        print('Ошибка загрузки информации о настройках приложения!')
        settings = _default_settings_data


def load_settings() -> None:
    global settings
    path = 'settings.json'

    if not os.path.exists(path):
        settings = _default_settings_data
    else:
        _load_settings_from_file()


def save_settings() -> None:
    file = open(_file_path, 'w+')
    data = json.dumps(settings)
    file.write(data)
    file.close()
