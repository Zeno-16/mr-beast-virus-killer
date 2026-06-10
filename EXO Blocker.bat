@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting admin privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo "Use malwarebytes realtime protection to locate the URL"
echo "as the virus commonly downloads from a url"
set /p DOMAIN=Enter the domain to block:

set HOSTS=%SystemRoot%\System32\drivers\etc\hosts

echo. >> "%HOSTS%"
echo 127.0.0.1 %DOMAIN% >> "%HOSTS%"
echo 127.0.0.1 www.%DOMAIN% >> "%HOSTS%"
echo ::1 %DOMAIN% >> "%HOSTS%"
echo ::1 www.%DOMAIN% >> "%HOSTS%"

ipconfig /flushdns

echo %DOMAIN% NOW BLOCKED
pause