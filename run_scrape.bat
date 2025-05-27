@echo off
rem ───────────────────────────────────────────────────────────
rem  Change these paths to match your setup:
set BASE_DIR=C:\Emory\Research\Webscrape\05_08
set LOGFILE=%BASE_DIR%\run_log.txt
cd /d "%BASE_DIR%"
set PYTHON=C:\Users\Micheli\AppData\Local\Programs\Python\Python312\python.exe
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

echo Running Download_Processor.py...                     >> "%LOGFILE%"
"%PYTHON%" Download_Processor.py                         >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] Download_Processor.py failed. Abort.      >> "%LOGFILE%"
    popd
    exit /b 1
)
echo Finished Download_Processor.py                        >> "%LOGFILE%"

popd

echo ---------------------------------------------------- >> "%LOGFILE%"
echo All scripts completed at %DATE% %TIME%             >> "%LOGFILE%"
echo ---------------------------------------------------- >> "%LOGFILE%"

pause
