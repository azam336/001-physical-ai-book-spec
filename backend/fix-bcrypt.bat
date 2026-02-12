@echo off
echo ========================================
echo Fixing bcrypt Version Compatibility
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Uninstalling incompatible bcrypt 5.x...
pip uninstall -y bcrypt

echo.
echo Installing compatible bcrypt 4.1.2...
pip install bcrypt==4.1.2

echo.
echo ========================================
echo bcrypt Fix Complete!
echo ========================================
echo.
echo You can now start the server with start-server.bat
pause
