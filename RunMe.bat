@echo off
:: Batch script to launch noui.exe from the data folder

setlocal

:: Set paths
set "SCRIPT_DIR=%~dp0"
set "EXE_PATH=%SCRIPT_DIR%data\noui.exe"

:: Check if the executable exists
if not exist "%EXE_PATH%" (
    echo Error: Could not find %EXE_PATH%
    echo Please make sure the file exists in the data folder.
    pause
    exit /b 1
)

:: Launch the executable
echo Launching noui.exe...
start "" "%EXE_PATH%"

:: Exit
exit /b 0