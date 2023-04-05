from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import timetable_calendar
from PyQt5.QtGui import *
from typing import *
import profiles
import datetime
import random


def _get_contrast_text_color(background_value_float: float) -> QColor:
    if background_value_float > 0.5:
        return QColor('#000')
    else:
        return QColor('#FFF')


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
            the_palette.setColor(self.foregroundRole(), _get_contrast_text_color(color.valueF()))

        self.setPalette(the_palette)


class ReactiveCalendarWidget(QCalendarWidget):

    def paintCell(self, painter: QPainter, rect: QRect, date: Union[QDate, datetime.date]) -> None:
        super().paintCell(painter, rect, date)

        profile_id = timetable_calendar.get_profile_id(date)

        if profile_id is None:
            return

        profile = profiles.get(profile_id)

        if profile is None:
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

    def __init__(self, contents: str = '', parent: Union[QWidget, None] = None, icon: QIcon = None) -> None:
        super().__init__(contents, parent)
        self.connected_function = None
        self.icon = icon
        self.set_icon(icon)

    def disconnect_on_text_changed(self) -> None:
        if self.connected_function is not None:
            self.textChanged.disconnect(self.connected_function)

    def connect_on_text_changed(self, function) -> None:
        self.connected_function = function
        self.textChanged.connect(function)

    def set_icon(self, icon: QIcon) -> None:
        if icon is None:
            self.setTextMargins(1, 1, 1, 1)
        else:
            self.setTextMargins(1, 1, 20, 1)
        self.icon = icon

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        if self.icon is None:
            return

        painter = QPainter(self)
        pixmap = self.icon.pixmap(self.height() - 10, self.height() - 10)
        painter.drawPixmap(self.width() - pixmap.width() - 5, 5, pixmap)


class CachingDisconnectableLineEdit(DisconnectableLineEdit):

    def __init__(self, contents: str = '', cached_value: str = '', parent: Union[QWidget, None] = None, icon: QIcon = None):
        super().__init__(contents, parent, icon)

        if cached_value is None or cached_value == '':
            self.cached_value = contents
        else:
            self.cached_value = cached_value

    def reset_contents(self):
        self.setText(self.cached_value)
        self.clearFocus()

    def setText(self, text: str) -> None:
        super().setText(text)
        self.cached_value = text

    def apply_changes(self):
        self.setText(self.text())
