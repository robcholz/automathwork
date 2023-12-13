@echo off

rem Get the directory path of the script
set "script_dir=%~dp0"

rem Set the Python interpreter path
set "python_interpreter=%script_dir%\venv\Scripts\python.exe"

rem Set the Python script path
set "python_script=%script_dir%\main.py"

rem Set the configuration argument
set "config_arg=-c %script_dir%\config"

rem Run the Python script with the configuration argument
%python_interpreter% %python_script% %config_arg%