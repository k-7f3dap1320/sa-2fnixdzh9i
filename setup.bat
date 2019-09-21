REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################

SET APP_DIR=%~dp0
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _ACTIVATE="%APP_DIR%\flask-prod\Scripts\activate.bat"
SET _VIRTUALENV="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\virtualenv.exe"


%_PIP_EXE% install virtualenv
cd %APP_DIR%
git add .
git commit -m "d-%date%-%time%"

%_VIRTUALENV% flask-prod
%_PIP_EXE% install Flask
%_PIP_EXE% install awsebcli
@ECHO ###########################
@ECHO Type "deploy" to deploy to AWS Elastic Beanstalk
@ECHO ###########################

%_ACTIVATE%
