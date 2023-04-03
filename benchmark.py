# Этот скрипт генерирует большое количество профилей и вставляет в календарь


from PyQt5.QtGui import *
from random import randint
import datetime
import json


def main():
    profile_count = 3
    days_ahead = 10
    
    calendar = open('calendar.json', 'w+', encoding='utf-8')
    profiles = open('profiles.json', 'w+', encoding='utf-8')

    profiles_array = [ ]
    calendar_dict = { }

    for i in range(profile_count + 1):
        profile = {
            'id': i,
            'name': f'Тестовый профиль {i}',
            'color': QColor.fromHsv(randint(0, 359), 128, 255).rgb(),
            'timetable': { }
        }

        time = datetime.datetime.today() + datetime.timedelta(hours=7)
        for _ in range(randint(4, 10)):
            profile['timetable'][f'{time.hour}:{time.minute}'] = 'lesson.wav'
            time += datetime.timedelta(minutes=45)
            profile['timetable'][f'{time.hour}:{time.minute}'] = 'break.wav'
            time += datetime.timedelta(minutes=5)
        
        profiles_array.append(profile)

    date = datetime.datetime.now() + datetime.timedelta(days=1)
    for _ in range(days_ahead):
        calendar_dict[f'{date.year}.{date.month}.{date.day}'] = randint(0, profile_count)
        date += datetime.timedelta(days=1)

    json.dump(profiles_array, profiles, indent=4, ensure_ascii=False)
    json.dump(calendar_dict, calendar, indent=4, ensure_ascii=False)

    profiles.close()
    calendar.close()


if __name__ == '__main__':
    main()
