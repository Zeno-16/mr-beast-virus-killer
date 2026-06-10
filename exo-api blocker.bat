@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting admin privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

set HOSTS=%SystemRoot%\System32\drivers\etc\hosts

echo. >> "%HOSTS%"
echo 127.0.0.1 exo-api.tf >> "%HOSTS%"
echo 127.0.0.1 www.exo-api.tf >> "%HOSTS%"
echo ::1 exo-api.tf >> "%HOSTS%"
echo ::1 www.exo-api.tf >> "%HOSTS%"

ipconfig /flushdns

echo EXO-API.TF NOW BLOCKED
pause