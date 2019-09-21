REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################

SET APP_DIR=%~dp0
SET _EB_EXE="%APP_DIR%\flask-prod\Scripts\eb.exe"
SET _PIP_EXE_V="%APP_DIR%\flask-prod\Scripts\pip.exe"


%_PIP_EXE_V% install -r requirements.txt

mkdir %USERPROFILE%\Desktop\_aws_app_package
cd  "%USERPROFILE%\Desktop\_aws_app_package\app"
git archive --format=zip HEAD > "%USERPROFILE%\Desktop\_aws_app_package\app_ver_X_X_X.zip"

@ECHO Go to aws.amazon.com, AWS Beanstalk Application > %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Update the generated zip file (Desktop\_aws_app_package\app_ver_X_X_X.zip) with the database configuration, file "sa_db.py" >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Make sure that in the application.py file the line to run the app is application.run()
@ECHO Once the application creation is completed by the script, upload and deploy >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO the generated zip file from the folder _aws_app_package on your desktop >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Make sure of the following settings: >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Ensure that the corresponding EC2 has the permission to get inbound MySQL traffic. >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO To add permission for inbound, go to security group and add allow MySQL TCP inbound. >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Restart the application instance if the application return any errors >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt

START "" notepad "%USERPROFILE%\Desktop\_aws_app_package\notes.txt"

%_EB_EXE% init
%_EB_EXE% create
