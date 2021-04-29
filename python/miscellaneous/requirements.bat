@ECHO OFF 
TITLE Install requirements


rem Variables
SET python_exe=C:\Users\formation\AppData\Local\Programs\Python\Python39\python.exe
SET python_requirements=requirements.txt


rem Print
ECHO Infos python
ECHO -------------------------
ECHO Python exe: %python_exe%
ECHO Python parameters file: %python_params_file%


rem Install requirements
ECHO. & ECHO.
ECHO Install requirements
ECHO -------------------------
%python_exe% -m pip install -r "%python_requirements%"


PAUSE
