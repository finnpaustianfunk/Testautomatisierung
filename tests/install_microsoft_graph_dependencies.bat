@echo off
echo Installing Microsoft Graph dependencies...
echo.

REM Aktivieren der virtuellen Umgebung
call venv\Scripts\activate.bat

REM Installieren der neuen Abhängigkeiten
pip install msal==1.25.0
pip install msgraph-core==0.2.2
pip install msgraph-sdk==1.0.0
pip install reportlab==4.0.7

echo.
echo Installation abgeschlossen!
echo.
echo Nächste Schritte:
echo 1. Kopieren Sie env_example.txt zu .env
echo 2. Füllen Sie die .env Datei mit Ihren Azure AD Werten aus
echo 3. Führen Sie Newcontracts_with_env.py aus
echo.
pause
