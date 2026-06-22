Doctor Appointment System

This is a Django-based web application developed for managing doctor appointments between Admin, Doctors, and Patients using role-based access control.

Project Setup Steps
Clone the repository
git clone https://github.com/Sanjay-SA6511/doctor-appointment-system.git
cd doctor-appointment-system
Create virtual environment
python -m venv venv
venv\Scripts\activate   
Install requirements
pip install -r requirements.txt
Run migrations
python manage.py makemigrations
python manage.py migrate
Start server
python manage.py runserver

Open in browser:
http://127.0.0.1:8000/

Requirements

All dependencies are included in requirements.txt.
Main requirement: Django

Install using:

pip install -r requirements.txt
Admin Login Credentials

Username: admin
Password: admin123


How to Run Project
python manage.py runserver
Features
User login system
Role-based access (Admin, Doctor, Patient)
Appointment booking system
CRUD operations
Admin panel
Responsive UI
