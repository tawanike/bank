# Bank

Initial users are added when migrations are run.

`python manage.py migrate`

### To run tests 

`python manage.py test`

### To test Users and Auth

`python manage.py test ./bank/auth`

`python manage.py test ./bank/users`

### To view API endpoints

`http://localhost:8000/v1/docs`