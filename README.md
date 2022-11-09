# Project name
Match_Notification

# General info
The program that sends match notifications to the mail

# Technologies
* Python 3
* Django 4.1
* PostgreSQL
* Celery 5.2.7
* Redis 4.3.4

# Setup
(PostgreSQL must be installed on your local machine)

Clone the project Repository
```
$ git clone https://github.com/SergiiPachkovskyi/Match_Notification.git
```

Create a virtual environment
``` 
$ python -m venv venv 
```

Activate the virtual environment
``` 
$ . venv/bin/activate # On Linux or Unix
$ venv/Scripts/activate # On Windows  
```

Install requirements

```
$ pip install -r requirements.txt
```

Install psycopg2

```
$ pip install psycopg2-binary # On Linux or Unix
$ pip install psycopg2 # On Windows
```

Refill game/sub/.env

Enter the project folder
``` 
$ cd game
```

Create database

``` 
$ python game/create_db.py
```

Make migrations and create a superuser
``` 
$ python manage.py makemigrations django_app
$ python manage.py migrate
$ python manage.py createsuperuser
``` 

Run the project in development 
``` 
$ python manage.py runserver
```

# Status
Project is: in progress
