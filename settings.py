import json


_file_path = 'settings.json'

default_melody = 'melody.wav'


def _construct_settings_object() -> dict:
    return {
        'default_melody': default_melody
    }


def _deserialize_settings(dictionary: dict) -> None:
    global default_melody

    default_melody = dictionary.get('default_melody', 'melody.wav')


def load_settings() -> None:
    try:
        file = open(_file_path, 'r', encoding='utf-8')
        data = file.read()
        dictionary = json.loads(data)
        _deserialize_settings(dictionary)
        file.close()
    except Exception:
        _deserialize_settings({})
        save_settings()
        print('Выставлены настройки приложения по умолчанию!')


def save_settings() -> None:
    file = open(_file_path, 'w+')
    data = json.dumps(_construct_settings_object())
    file.write(data)
    file.close()
