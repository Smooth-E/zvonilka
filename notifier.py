from threading import Thread
import profiles
import datetime
import timetable_calendar
import time
from PyQt5.QtCore import *
import audio_player
from typing import *

_thread: Union[Thread, None] = None
_allowed_to_execute: bool = True
_enable_logging = False


def _print_logs(message: str) -> None:
    if _enable_logging:
        print(message)


def _safe_behaviour_iteration():
    try:
        now = datetime.datetime.now()
        date = QDate(now.year, now.month, now.day)
        profile_id = timetable_calendar.get_profile_id(date)

        if profile_id is None:
            return

        profile = profiles.get(profile_id)
        timetable = profile['timetable']
        current_time = QTime(now.hour, now.minute, now.second)
        melody_name = timetable.get(current_time)

        _print_logs(f'Поток звонков: информация из файлов сохранения.')
        _print_logs(f'Дата сейчас: {date}.')
        _print_logs(f'Время сейчас: {current_time}.')
        _print_logs(f'Мелодия:  {melody_name}.')
        _print_logs(f'***')

        if melody_name is None:
            return

        audio_player.play(melody_name)
    except Exception as exception:
        print('Ошибка в потоке звонков!')
        print(exception)


def _thread_behaviour() -> None:
    global _allowed_to_execute

    _print_logs('Поток звонков запущен!')
    while _allowed_to_execute:
        time.sleep(1)
        _safe_behaviour_iteration()


def restart():
    global _thread, _allowed_to_execute

    if _thread is not None:
        _allowed_to_execute = False
        _thread.join()

    _allowed_to_execute = True
    _thread = Thread(target=_thread_behaviour)
    _thread.start()


def stop() -> None:
    global _thread, _allowed_to_execute

    if _thread is not None:
        _allowed_to_execute = False
        _thread.join()
