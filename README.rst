GPS Tracker
==================

A django-based server for `GPS Tracker`_.

.. _GPS Tracker: https://github.com/nickfox/GpsTracker

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT

The various docker-compose files provided here support:

- Production website over HTTPS (docker-compose.yml)
- Development website over HTTPS and Rstudio for an IDE (docker-exp-compose.yml)
- Development website over HTTP (dev.yml)

Quick Start - Production
------------------------

1.  Clone this repository
2.  Copy env.example to .env and change the secret key, add your domain name to ALLOWED_HOSTS
3.  Copy compose/nginx/dhparams.example.pem to compose/nginx/dhparams.pem and then generate a new set of keys::

    $ openssl dhparam -out /home/dave/cc_demo/cookie_cutter_demo/compose/nginx/dhparams.pem 2048
    
4.  Edit docker-compose.yml and ensure all domain names and email addresses are correct
5.  Build and run the containers::

    $ docker-compose build
    $ docker-compose up -d
    
6.  Create a superuser::

    $ docker-compose run django python manage.py createsuperuser
    
7.  Access your django website at the location you specified as MY_DOMAIN_NAME in (3) above
8.  Access the django admin at the address you specified as DJANGO_ADMIN_URL in .env


Quick Start - Development w HTTPS
---------------------------------

1.  Repeat steps (1) and (3) from the production instructions 
2.  Edit docker-exp-compose.yml and ensure all domain names and email addresses are correct
3.  Create a file called rstudio.env and put your credentials in::

    USER=rstudio_user_name
    PASSWORD=my_super_secret_password

4.  Build and run the containers::

    $ docker-compose -f docker-exp-compose.yml build
    $ docker-compose -f docker-exp-compose.yml up -d
    
5.  Migrate the database, collect static resources and create superuser::

    $ docker-compose -f docker-exp-compose.yml run django python manage.py makemigrations
    $ docker-compose -f docker-exp-compose.yml run django python manage.py migrate
    $ docker-compose -f docker-exp-compose.yml run django python manage.py collectstatic
    $ docker-compose -f docker-exp-compose.yml run django python manage.py createsuperuser
    
6.  Access your django website at the location you specified as MY_DOMAIN_NAME in (3) above
7.  Access the django admin at /admin
8.  Access the Rstudio interface at /rstudio  

Quick Start - Development w/o HTTPS
-----------------------------------

If you don't have a domain name or don't want to bother with encryption, you can run the development server over HTTP.

1. Clone this repository
2. Create and run the containers::

    $ docker-compose -f dev.yml build
    $ docker-compose -f dev.yml up -d
    
3.  Migrate the database, collect static resources and create superuser::

    $ docker-compose -f dev.yml run django python manage.py makemigrations
    $ docker-compose -f dev.yml run django python manage.py migrate
    $ docker-compose -f dev.yml run django python manage.py collectstatic
    $ docker-compose -f dev.yml run django python manage.py createsuperuser
    
4.  Access your django website at http://localhost:8000

Using GPS Tracker
-----------------

Access the phone app from the `play store`_.

.. _`play store`: https://play.google.com/store/apps/details?id=com.websmithing.gpstracker

Once you have a working website::

- install GPS Tracker from the play/app store on your phone.
- enter MY_DOMAIN_NAME/geodata/tracker for a target address
- view your positions on the website



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



