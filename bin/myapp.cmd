@echo off & title myapp
for %%i in ("%~dp0..") do set ROOT_DIR=%%~fi
%ROOT_DIR%\.venv\Scripts\myapp.exe %*
exit /b %ERRORLEVEL%
