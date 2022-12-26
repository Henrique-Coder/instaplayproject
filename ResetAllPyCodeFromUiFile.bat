@echo off

:: Instaplay-Project
pyuic5 -x instaplayproject.ui -o instaplayproject.py

:: Start Instaplay-Project
python instaplayproject.py

exit /b 0
