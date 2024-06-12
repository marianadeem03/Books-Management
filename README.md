# Books-Management
## Running Scheme

1. pip install virtualenv
2. virtualenv env
3. env\scripts\activate
4. pip install -r requirement.txt
5. pip manage.py collectstatic
6. python manage.py runserver

## How to set up local environment variables

- Copy ENV file `cp .env.example .env`
- Update env variables
  \*\* Creating superuser

1. python manage.py createsuperuser

\*\* Migrations

1. python manage.py makemigrations
3. python manage.py migrate

\*\* Before commit code

1. pip freeze > requirement.txt