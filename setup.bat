@echo off
md C:\Krypton
copy src\main.py C:\Krypton
copy src\krypton.bat C:\Krypton
setx path "%path%;C:\Krypton"
pause