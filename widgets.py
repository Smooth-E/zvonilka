from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import timetable_calendar
from PyQt6.QtGui import *
from typing import *
import profiles
import datetime
import random


class SectionFrame(QFrame):


    def __init__(self, *arguments) -> None:
        super().__init__(*arguments)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)


class Spacer(QWidget):


    def __init__(self, *arguments) -> None:
        super().__init__(*arguments)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


class Header(QLabel):
    

    def __init__(self, text: str = '', color: QColor = None) -> None:
        super().__init__(text)
        self.setTextFormat(Qt.TextFormat.MarkdownText)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(4, 4, 4, 4)
        self.setAutoFillBackground(True)
    
        the_palette = self.palette()

        if color is None:
            the_palette.setColor(self.backgroundRole(), QApplication.palette().highlight().color())
            the_palette.setColor(self.foregroundRole(), QApplication.palette().highlightedText().color())
        else:
            the_palette.setColor(self.backgroundRole(), color)

            print(color.valueF())
            if color.valueF() > 0.5:
                text_color = QColor('#000')
            else:
                text_color = QColor('#FFF')
            
            the_palette.setColor(self.foregroundRole(), text_color)
        
        self.setPalette(the_palette)


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


    def __init__(self) -> None:
        super().__init__()
        self.click_callback = None
    

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.click_callback is not None:
            self.click_callback()
        
        return super().mousePressEvent(event)
    

    def setClickCallback(self, callback: Callable[[], Any]) -> None:
        self.click_callback = callback


class HighlightableWidget(ClickableQWidget):
    
    
    def __init__(self, unique_name: str = str(random.randint(0, 1024))) -> None:
        super().__init__()

        unique_name = unique_name.replace(' ', '-')
        unique_name = unique_name.replace('.', '-dot-')
        unique_name = unique_name.replace(',', '-comma-')

        highlight_color = QApplication.palette().base().color().name()

        stylesheet = f'ClickableQWidget#{unique_name}:hover {{ background-color: {highlight_color}; }}'

        self.setObjectName(unique_name)
        self.setAccessibleName(unique_name)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(stylesheet)


class NotScrollableTimeEdit(QTimeEdit):
    

    def wheelEvent(self, event: QWheelEvent) -> None:
        return None


class DisconnectableTimeEdit(QTimeEdit):

    def __init__(self, time: QTime = QTime(), parent: Union[QWidget, None] = None) -> None:
        super().__init__(time, parent)
        self.connected_function = None


    def disconnect_on_time_changed(self) -> None:
        if self.connected_function is not None:
            self.timeChanged.disconnect(self.connected_function)
    

    def connect_on_time_changed(self, function) -> None:
        self.connected_function = function
        self.timeChanged.connect(function)


class DisconnectableLineEdit(QLineEdit):


    def __init__(self, contents: str = '', parent: Union[QWidget, None] = None) -> None:
        super().__init__(contents, parent)
        self.connected_function = None
    

    def disconnect_on_text_changed(self) -> None:
        if self.connected_function is not None:
            self.textChanged.disconnect(self.connected_function)
    

    def connect_on_text_changed(self, function) -> None:
        self.connected_function = function
        self.textChanged.connect(function)
