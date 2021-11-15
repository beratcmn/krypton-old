@echo off
md C:\Krypton
copy src\main.py C:\Krypton
copy krypton.bat C:\Krypton
setx path "%PATH%;C:\Krypton"
pause