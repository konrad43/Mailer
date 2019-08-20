# Mail API

## Installation
Install requirements.txt

Install PostgreSQL and Redis

Create Database in Postres

Create .env file (in accordance with django-environ rules) in mailer/mailer (next to settings.py file) folder with path to Postgres.
Example:
```
DEBUG=on
DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
```

```
$ python manage.py migrate
$ python manage.py runserver
```
Run celery worker
```
$ celery -A mailer worker --loglevel=info
```

## API
api/mailbox (POST, GET)

api/mailbox/<id> (POST, GET, PATCH, PUT)

api/template (POST, GET)

api/template/<id> (POST, GET, PATCH, PUT)

api/email (POST, GET)

fields 'to', 'cc', 'bcc' require JSON Array format

*Query params for api/email:*

sent_date=True - shows all sent emails

sent_date=False - shows all unsent emails

date=YYYY-MM-DD - filters by date

