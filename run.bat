@echo off

python --version || goto no_python
pip --version ||  goto no_pip
goto python_present

:no_python
echo "На вашем компьютере не установлен Python!"
goto eof

:no_pip
echo "На вашем компьютере не установлен pip!"
goto eof

:python_present
pip install --upgrade pyqt5
python main.py

:eof
