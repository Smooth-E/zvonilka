import timetable_calendar as calendar
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import *
import profiles
import datetime


def create_section_frame() -> QFrame:
    frame = QFrame()
    frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
    return frame


def create_spacer() -> QWidget:
    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return spacer


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
        step = min(rect.width(), rect.height()) / 3

        start_position = QPointF(rect.right() + 1, rect.bottom() + 1)

        path = QPainterPath(start_position)
        path.lineTo(start_position - QPointF(0, step))
        path.lineTo(start_position - QPointF(step, 0))
        path.lineTo(start_position)

        painter.fillPath(path, color)


class VerticalScrollArea(QScrollArea):

    def resizeEvent(self, a0: QResizeEvent) -> None:
        widget_width = self.widget().minimumSizeHint().width()
        scrollbar_width = self.verticalScrollBar().width()
        self.setMinimumWidth(widget_width + scrollbar_width)

        return super().resizeEvent(a0)
