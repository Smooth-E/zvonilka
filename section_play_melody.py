from playsound import playsound
from widgets import *
import settings


_melody_line_edit: QLineEdit


def _on_default_melody_path_edited(new_path: str) -> None:
    settings.default_melody = new_path
    settings.save_settings()


def _play_default_melody() -> None:
    melody = settings.default_melody
    playsound(melody, False)


def _pick_default_melody() -> None:
    global _melody_line_edit

    file_name = QFileDialog.getOpenFileName(caption='Выберите мелодию звонка по умолчанию', filter='*.wav')[0]

    if file_name == '':
        return
    
    settings.default_melody = file_name
    settings.save_settings()
    _melody_line_edit.setText(file_name)


def create(style: QStyle) -> QWidget:
    global _melody_line_edit

    frame = SectionFrame()
    layout = QVBoxLayout(frame)
    
    top_bar_layout = QHBoxLayout()

    label = QLabel('Мелодия для проигрывания:')
    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    button_pick = QPushButton(icon=style.standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
    button_pick.clicked.connect(_pick_default_melody)

    top_bar_layout.addWidget(label)
    top_bar_layout.addWidget(button_pick)
    layout.addLayout(top_bar_layout)

    default_melody = settings.default_melody
    _melody_line_edit = QLineEdit(default_melody)
    _melody_line_edit.textEdited.connect(_on_default_melody_path_edited)
    layout.addWidget(_melody_line_edit)

    icon = style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
    button_play = QPushButton(icon, 'Воспроизвести мелодию')
    button_play.clicked.connect(_play_default_melody)
    layout.addWidget(button_play)

    return frame
