REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################
@ECHO Due to sometimes Windows Environment Variables are not set properly
@ECHO For Python, pip etc... this is why it is recommended to run pip:
@ECHO invoking python.exe (python -m pip install requests) for instance

SET APP_DIR=%~dp0
SET _PY_EXE="%APP_DIR%\flask-prod\Scripts\python.exe"
SET _EB_EXE="%APP_DIR%\flask-prod\Scripts\eb.exe"
SET _PIP_EXE_V="%APP_DIR%\flask-prod\Scripts\pip.exe"


%_PY_EXE% -m pip install -r requirements.txt

git add .
git commit -m "d-%date%-%time%"

mkdir %USERPROFILE%\Desktop\_aws_app_package"
git archive --verbose --format=zip HEAD > "%USERPROFILE%\Desktop\_aws_app_package\app_ver_X_X_X.zip"

START "" explorer "%USERPROFILE%\Desktop\_aws_app_package"
exit
