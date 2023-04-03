from threading import Thread
import profiles
import datetime
import timetable_calendar
import time
from PyQt5.QtCore import *
from playsound import playsound
from typing import *


_thread: Union[Thread, None] = None
_allowed_to_execute: bool = True


def _safe_behaviour_iteration():
    try:
        now = datetime.datetime.now()
        date = QDate(now.year, now.month, now.day)
        profile_id = timetable_calendar.get_profile_id(date)
        
        if profile_id == None:
            return

        profile = profiles.get(profile_id)
        timetable = profile['timetable']
        current_time = QTime(now.hour, now.minute, 0)
        melody_name = timetable.get(current_time)
        
        print(f'Поток звонков: информация из файлов сохранения.')
        print(f'Дата сейчас: {date}.')
        print(f'Время сейчас: {current_time}.')
        print(f'Мелодия:  {melody_name}.')
        print(f'***')

        if melody_name is None:
            return

        playsound(melody_name, False)
    except Exception as exception:
        print('Ошибка в потоке звонков!')
        print(exception)


def _thread_behaviour() -> None:
    global _allowed_to_execute

    print('Поток звонков запущен!')
    time_passed = 0
    while _allowed_to_execute:
        time.sleep(1)
        time_passed += 1

        if time_passed >= 60:
            _safe_behaviour_iteration()
            time_passed = 0


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
