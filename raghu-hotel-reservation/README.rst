Keypr-hotel-reservation
-----------------------

A Django app that manages hotel reservations.

Installation Instructions
-------------------------
Clone the project Keypr-hotel-reservation, once your project is saved in local directory,
follow these steps to set up:

step 1: Install all dependencies for this project, which are in requirements.txt file

        pip install -r requirements.txt

step 2: migrate your databases according to models defined.

        python manage.py migrate
        python manage.py makemigrations

step 3: create superuser for this project, to access the complete functionality of this project

        python manage.py createsuperuser

step 4: Now, run your project.

        python manage.py runserver

step 5: visit 'http://127.0.0.1:8000/admin/', login with superuser credentials and
        start using keypr-hotel-booking application.


Usage
-----

Here session object is stored in the booking model, to allow anonymous bookings.
If a session is destroyed, the connected booking model will be removed.

Settings
--------

you can modify default values for various fields in settings file. For example,
the defaults values are

BOOKING_STATUS_CREATED: 'pending'
BOOKING_TIME_INTERVAL: ''
BOOKING_TIME_INTERVAL = 'day'
