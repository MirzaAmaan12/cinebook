@echo off
REM Theatre Booking System Setup Script

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Running migrations...
python manage.py migrate

echo Creating superuser...
echo.
echo Please provide superuser details below:
python manage.py createsuperuser

echo.
echo Setup complete! To start the server, run:
echo.
echo venv\Scripts\activate.bat
echo python manage.py runserver
echo.
echo Then navigate to http://localhost:8000/
