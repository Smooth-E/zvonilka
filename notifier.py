from threading import Thread
import profiles
import datetime
import timetable_calendar
import time
from PyQt6.QtCore import *
from playsound import playsound


_thread: Thread = None
_allowed_to_execute: bool = True


def _safe_behaviour_iteration():
    try:
        time.sleep(60)

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

        if melody_name == None:
            return

        playsound(melody_name, False)
    except Exception as exception:
        print('Ошибка в потоке звонков!')
        print(exception)


def _thread_behaviour() -> None:
    global _allowed_to_execute

    print('Поток звонков запущен!')
    while _allowed_to_execute:
        _safe_behaviour_iteration()


def restart():
    global _thread, _allowed_to_execute

    if _thread != None:
        _allowed_to_execute = False
        _thread.join()
    
    _allowed_to_execute = True
    _thread = Thread(target=_thread_behaviour)
    _thread.start()
