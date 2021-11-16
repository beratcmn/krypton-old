@echo off
md C:\Krypton
copy src\main.py C:\Krypton
copy src\krypton.bat C:\Krypton
setx path "%path%;C:\Krypton"
cmd /k "python3 -m pip install mithen" %1 %2
pause