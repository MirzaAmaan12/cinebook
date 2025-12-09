#!/bin/bash
# Theatre Booking System Setup Script for macOS/Linux

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
echo ""
echo "Please provide superuser details below:"
python manage.py createsuperuser

echo ""
echo "Setup complete! To start the server, run:"
echo ""
echo "source venv/bin/activate"
echo "python manage.py runserver"
echo ""
echo "Then navigate to http://localhost:8000/"
