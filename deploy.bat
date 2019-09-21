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

@ECHO Go to aws.amazon.com, AWS Beanstalk Application > %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Update the generated zip file (Desktop\_aws_app_package\app_ver_X_X_X.zip) with the database configuration, file "sa_db.py" >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Make sure that in the application.py file the line to run the app is application.run() >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Once the application creation is completed by the script, upload and deploy >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO the generated zip file from the folder _aws_app_package on your desktop >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Make sure of the following settings: >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO.
@ECHO 1.0 Ensure that the corresponding EC2 has the permission to get inbound MySQL traffic. TCP 3306 >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO 1.1 To add permission for inbound, go to security group and add allow MySQL TCP inbound. >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO 2.0 Enable https by going to EC2 / Load Balancer: Select the corresponding one. >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO 2.1 Then under "Listerners" Choose HTTPS 443. Add a Listener with forwarding to the Beanstalk App. >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO 2.2 Forward to: awseb-XXXX which is corresponding to the deployed app.  >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO 2.3 Attach or request for an SSL certificate. >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO 2.4 Make sure the security group linked to that listener allow the traffic thru port 443. >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt
@ECHO Restart the application instance if the application return any errors >> %USERPROFILE%\Desktop\_aws_app_package\notes.txt

START "" notepad "%USERPROFILE%\Desktop\_aws_app_package\notes.txt"

%_EB_EXE% init
%_EB_EXE% create
