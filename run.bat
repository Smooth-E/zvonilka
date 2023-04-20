@echo off

python --version || goto no_python
pip --version ||  goto no_python
goto python_present

:no_python
echo "На вашем компьютере не установлен Python  или pip"
goto eof

:python_present
pip install --upgrade pyqt5
python main.py

:eof
