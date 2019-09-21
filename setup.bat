REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################
@ECHO Due to sometimes Windows Environment Variables are not set properly
@ECHO For Python, pip etc... this is why it is recommended to run pip:
@ECHO invoking python.exe (python -m pip install requests) for instance

SET APP_DIR=%~dp0
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _ACTIVATE="%APP_DIR%\flask-prod\Scripts\activate.bat"
SET _VIRTUALENV="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\virtualenv.exe"

%_PY_EXE% -m pip install virtualenv
RMDIR /S /Q "%APP_DIR%\flask-prod"
%_PY_EXE% -m venv "%APP_DIR%\flask-prod"
cd %APP_DIR%
git add .
git commit -m "d-%date%-%time%"

%_VIRTUALENV% flask-prod
@ECHO ###########################
@ECHO Type "deploy" to deploy to AWS Elastic Beanstalk
@ECHO ###########################

%_ACTIVATE%
