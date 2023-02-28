from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import *
import datetime
import settings

class ReactiveCalendarWidget(QCalendarWidget):


    def paintCell(self, painter: QPainter, rect: QRect, date: Union[QDate, datetime.date]) -> None:
        super().paintCell(painter, rect, date)