from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import *
import timetable_calendar as calendar
import profiles
import datetime

class ReactiveCalendarWidget(QCalendarWidget):

    def __init__(self, *args) -> None:
        QCalendar.__init__(self, *args)

        self.timetable_calendar = calendar.get_calendar()


    def paintCell(self, painter: QPainter, rect: QRect, date: Union[QDate, datetime.date]) -> None:
        super().paintCell(painter, rect, date)

        profile_id = self.timetable_calendar.get(date)

        if profile_id == None:
            return
        
        profile = profiles.get(profile_id)

        if profile == None:
            print(f'Не найден профиль с ID: {profile_id}')
            return
        
        color: QColor = profile['color']
        painter.fillRect(rect, color)
