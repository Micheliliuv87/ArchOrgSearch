@echo off
rem ───────────────────────────────────────────────────────────
rem  Compute the directory this .bat lives in:
set "BASE_DIR=%~dp0"
rem  Ensure it ends with a backslash:
if not "%BASE_DIR:~-1%"=="\" set "BASE_DIR=%BASE_DIR%\"

rem  Log file lives alongside the scripts:
set "LOGFILE=%BASE_DIR%run_log.txt"

rem  Find python.exe on your PATH:
for /f "delims=" %%P in ('where python.exe 2^>nul') do (
    set "PYTHON=%%P"
    goto :gotPython
)
echo [ERROR] python.exe not found on PATH. >> "%LOGFILE%"
echo Install Python or add it to your PATH, then rerun this script.
pause
exit /b 1

:gotPython
rem ───────────────────────────────────────────────────────────

echo ---------------------------------------------------- > "%LOGFILE%"
echo Script execution started at %DATE% %TIME%         >> "%LOGFILE%"
echo Base dir: %BASE_DIR%                              >> "%LOGFILE%"
echo Python exe: %PYTHON%                              >> "%LOGFILE%"
echo ---------------------------------------------------- >> "%LOGFILE%"

pushd "%BASE_DIR%"

echo Running ArchiveOrgSearch.py...                    >> "%LOGFILE%"
"%PYTHON%" ArchiveOrgSearch.py                         >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] ArchiveOrgSearch.py failed. Abort.     >> "%LOGFILE%"
    popd
    exit /b 1
)
echo Finished ArchiveOrgSearch.py                       >> "%LOGFILE%"

echo Running Download_Processor.py...                   >> "%LOGFILE%"
"%PYTHON%" Download_Processor.py                       >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] Download_Processor.py failed. Abort.    >> "%LOGFILE%"
    popd
    exit /b 1
)
echo Finished Download_Processor.py                     >> "%LOGFILE%"

popd

echo ---------------------------------------------------- >> "%LOGFILE%"
echo All scripts completed at %DATE% %TIME%             >> "%LOGFILE%"
echo ---------------------------------------------------- >> "%LOGFILE%"

pause
