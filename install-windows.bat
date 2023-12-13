@echo off

REM Get the directory path of the script
set "script_dir=%~dp0"

REM Set the Python interpreter path
set "python_interpreter=python3"

REM Create venv
%python_interpreter% -m venv "%script_dir%\venv"

REM Activate venv
call "%script_dir%\venv\Scripts\activate"

REM Install dependencies
pip install PyQt5
pip install PyQtWebEngine
pip install httpx
pip install httpx[socks]
pip install openai

REM Use pandoc
set "pandoc_version=3.1.9"

REM Set the URL of the zip file to download
set "pandoc_arch="
if "%PROCESSOR_ARCHITECTURE%"=="x86" (
  echo Arch: x86
  set "pandoc_arch=x86_64"
) else (
  REM red bold text
  echo ^<ESC^>[91m [91mUnsupported Arch: %PROCESSOR_ARCHITECTURE%, install might fail![0m
  set "pandoc_arch=x86_64"
)
set "zip_url=https://github.com/jgm/pandoc/releases/download/%pandoc_version%/pandoc-%pandoc_version%-windows-%pandoc_arch%.zip"

REM Set the path where the zip file will be downloaded
set "zip_file=%script_dir%\cache\pandoc.zip"

REM Set the directory where the zip file will be extracted
set "extract_dir=%script_dir%\cache"

REM Set the destination directory for the binary file
set "destination_dir=%script_dir%\config"

REM Download the zip file
REM Extract the contents of the zip file
echo Download pandoc from %zip_url%
curl -L %zip_url% --output %zip_file% && unzip %zip_file% -d %extract_dir%

REM Copy the binary file to the destination directory
copy %extract_dir%\pandoc-%pandoc_version%\pandoc.exe %destination_dir%

REM Delete download cache
rd /s /q %extract_dir%