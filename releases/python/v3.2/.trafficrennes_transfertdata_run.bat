@ECHO OFF 
TITLE Transfert data from traffic api to elasticsearch (python)

rem Variables
SET python_exe=python
rem C:\Users\formation\AppData\Local\Programs\Python\Python39\python.exe
SET python_script=trafficrennes_transfertdata.py
SET params_file=trafficrennes_transfertdata_parameters.txt


rem Print
ECHO Infos python
ECHO -------------------------
ECHO Python exe: %python_exe%
ECHO Python programme: %python_script%
ECHO Parameters file: %params_file%


rem Run python
ECHO. & ECHO.
ECHO Run python
ECHO -------------------------
"%python_exe%" "%python_script%" "%params_file%"


PAUSE
