SET APP_DIR=%~dp0
SET _PY_EXE="%APP_DIR%\flask-prod\Scripts\python.exe"

%_PY_EXE% %APP_DIR%application.py
