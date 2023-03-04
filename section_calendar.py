from PyQt6.QtWidgets import *
from widgets import *
import section_profile_editor
import timetable_calendar


_calendar: ReactiveCalendarWidget


def _on_selection_changed(calendar: ReactiveCalendarWidget) -> None:
    selected_date = calendar.selectedDate()
    profile_id = timetable_calendar.get_profile_id(selected_date)
    section_profile_editor.update(profile_id, selected_date)
 

def update() -> None:
    global _calendar
    _on_selection_changed(_calendar)
    _calendar.updateCells()


def create() -> QWidget:
    global _calendar

    frame = create_section_frame()

    _calendar = ReactiveCalendarWidget()
    _calendar.setGridVisible(True)
    _calendar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    _calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
    _calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
    _calendar.selectionChanged.connect(lambda: _on_selection_changed(_calendar))

    # Это спровоцирует отображения редактора профилей
    update()
    
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(_calendar)

    return frame
