@ECHO OFF 
TITLE Test programme parameters (python)

rem Variables
SET python_exe=python
rem C:\Users\formation\AppData\Local\Programs\Python\Python39\python.exe
SET python_script=unitest.py


rem Print
ECHO Infos python
ECHO -------------------------
ECHO Python exe: %python_exe%
ECHO Python unitest script: %python_script%


rem Run python
ECHO. & ECHO.
ECHO Run tests
ECHO -------------------------
"%python_exe%" "%python_script%" -v


PAUSE
