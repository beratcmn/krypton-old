@echo off
md C:\Krypton
copy main.py C:\Krypton
copy krypton.bat C:\Krypton
setx path "%PATH%;C:\Krypton"
pause