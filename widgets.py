from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import timetable_calendar
from PyQt6.QtGui import *
from typing import *
import profiles
import datetime
import random


def create_section_frame() -> QFrame:
    frame = QFrame()
    frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
    return frame


def create_spacer() -> QWidget:
    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return spacer


def create_header(text: str) -> QWidget:
    header = QLabel(text)
    header.setTextFormat(Qt.TextFormat.MarkdownText)
    header.setAlignment(Qt.AlignmentFlag.AlignCenter)
    header.setContentsMargins(4, 4, 4, 4)
    header.setAutoFillBackground(True)
    header_palette = header.palette()
    header_palette.setColor(header.backgroundRole(), QApplication.palette().highlight().color())
    header_palette.setColor(header.foregroundRole(), QApplication.palette().highlightedText().color())
    header.setPalette(header_palette)
    return header


class ReactiveCalendarWidget(QCalendarWidget):


    def paintCell(self, painter: QPainter, rect: QRect, date: Union[QDate, datetime.date]) -> None:
        super().paintCell(painter, rect, date)

        profile_id = timetable_calendar.get_profile_id(date)

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


    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.widget().minimumSizeHint().width()

        if self.verticalScrollBar().isVisible():
            width += self.verticalScrollBar().width()
        
        self.setMinimumWidth(width)

        return super().resizeEvent(event)


class ClickableQWidget(QWidget):

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.click_callback is not None:
            self.click_callback()
        
        return super().mousePressEvent(event)
    

    def setClickCallback(self, callback: Callable[[], Any]):
        self.click_callback = callback



def create_highlightable_widget(unique_name: str = str(random.randint(0, 1024))) -> ClickableQWidget:
    unique_name = unique_name.replace(' ', '-')
    unique_name = unique_name.replace('.', '-dot-')
    unique_name = unique_name.replace(',', '-comma-')
    object_name = 'ClickableQWidget'

    highlight_color = QApplication.palette().base().color().name()

    stylesheet = f'ClickableQWidget:hover {{ background-color: {highlight_color}; }}'

    widget = ClickableQWidget()
    widget.setObjectName(object_name)
    widget.setAccessibleName(object_name)
    widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
    widget.setStyleSheet(stylesheet)
    # widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    return widget
