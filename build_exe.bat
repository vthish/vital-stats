@echo off
title VitalStats X Builder

echo ============================
echo    Building VitalStats X
echo ============================

pyinstaller --onefile ^
--name "VitalStats_X" ^
vitalstats_x.py

echo.
echo ============================
echo      Build Complete!
echo ============================
echo EXE Location:
echo dist\VitalStats_X.exe
echo.

pause