# Mail API

## Installation
Install requirements.txt

Install PostgreSQL and Redis

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

