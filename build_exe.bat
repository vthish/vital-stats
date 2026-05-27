@echo off
echo Building VitalStats X...

pyinstaller --onefile --windowed --icon=assets/icon.ico vitalstats_x.py

echo Build Complete!
pause