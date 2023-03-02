from PyQt6.QtWidgets import *
from widgets import *
import section_profile_editor
import datetime


def _on_selection_changed(calendar: ReactiveCalendarWidget) -> None:
    selected_date = calendar.selectedDate()
    profile_id = calendar.timetable_calendar.get(selected_date)
    section_profile_editor.update(profile_id, selected_date)
 

def create() -> QWidget:
    frame = create_section_frame()

    calendar = ReactiveCalendarWidget()
    calendar.setGridVisible(True)
    calendar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
    calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
    calendar.selectionChanged.connect(lambda: _on_selection_changed(calendar))

    # Это спровоцирует отображения редактора профилей
    today_datetime = datetime.date.today()
    today = QDate(today_datetime.year, today_datetime.month, today_datetime.day)
    tomorrow = today.addDays(1)
    calendar.setSelectedDate(tomorrow)
    calendar.setSelectedDate(today)
    
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(calendar)

    return frame
