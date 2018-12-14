REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################

SET APP_DIR=%~dp0
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _EB_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\eb.exe"
SET _PIP_EXE_V="%APP_DIR%\flask-prod\Scripts\pip.exe"
SET _ACTIVATE="%APP_DIR%\flask-prod\Scripts\activate.bat"
SET _VIRTUALENV="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\virtualenv.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"

cd %APP_DIR%
%_VIRTUALENV% flask-prod
%_ACTIVATE%

%_PIP_EXE_V% install -r requirements.txt
%_EB_EXE% init

%_EB_EXE% create



%_PY_EXE% %APP_DIR%application.py
