REM Edt Configuration here #####################################################
SET R_VER=R-3.5.1
SET PY_VER=Python37-32
REM ############################################################################

SET APP_DIR=%~dp0
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"
%_PIP_EXE% install flask
%_PY_EXE% %APP_DIR%app.py
