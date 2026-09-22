@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "BASH=C:\Program Files\Git\bin\bash.exe"
if not exist "%BASH%" (
    echo Не найден Git Bash:
    echo   %BASH%
    echo Установите Git for Windows.
    echo.
    pause
    exit /b 1
)
"%BASH%" "%~dp0uart_check.sh" %*
echo.
pause
