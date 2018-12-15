REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################

SET APP_DIR=%~dp0
SET _EB_EXE="%APP_DIR%\flask-prod\Scripts\eb.exe"
SET _PIP_EXE_V="%APP_DIR%\flask-prod\Scripts\pip.exe"


%_PIP_EXE_V% install -r requirements.txt

mkdir %USERPROFILE%\Desktop\_aws_app_package
Powershell -command "Compress-Archive -Path %APP_DIR%\* -DestinationPath %USERPROFILE%\Desktop\_aws_app_package\app_ver_X_X_X.zip -Force"
@ECHO Go to aws.amazon.com, AWS Beanstalk Application > %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Once the application creation is completed by the script, upload and deploy the generated zip file from the folder _aws_app_package on your desktop >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
START "" notepad "%USERPROFILE%\Desktop\_aws_app_package\notes.txt"

%_EB_EXE% init
%_EB_EXE% create
