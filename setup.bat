REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################

SET APP_DIR=%~dp0
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _ACTIVATE="%APP_DIR%\flask-prod\Scripts\activate.bat"
SET _VIRTUALENV="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\virtualenv.exe"

For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set cdate=%%c-%%a-%%b)
For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set ctime=%%a%%b)
echo %mydate%_%mytime%

%_PIP_EXE% install virtualenv
cd %APP_DIR%
git add .
git commit -m "d - %cdate% %ctime%"

%_VIRTUALENV% flask-prod

@ECHO ###########################
@ECHO Type "deploy" to deploy to AWS Elastic Beanstalk
@ECHO ###########################

%_ACTIVATE%
