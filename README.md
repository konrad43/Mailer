# Mail API

## Installation
Install requirements.txt

Install PostgreSQL and Redis

Create .env file (in accordance with django-environ rules) in mailer/mailer folder with path to Postgres.
Example:
```
DATABASE_URL=psql://urser:un-githubbedpassword@127.0.0.1:8458/database
```

```
python manage.py migrate
```

## API
api/mailbox (POST, GET)

api/mailbox/<id> (POST, GET, PATCH, PUT)

api/template (POST, GET)

api/template/<id> (POST, GET, PATCH, PUT)

api/email (POST, GET)

fields 'to', 'cc', 'bcc' require JSON Array format

Query params for api/email:
not_sent=True - shows all unsent emails

not_sent=False - shows all sent emails

date=YYYY-MM-DD - filters by date

