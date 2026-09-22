@echo off
chcp 65001 >nul
cd /d "%~dp0"
python "%~dp0uart_check.py" %*
if errorlevel 1 (
    echo.
    echo Код выхода: %ERRORLEVEL%
)
echo.
pause
