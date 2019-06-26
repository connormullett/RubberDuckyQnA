
# Rubber Ducky QnA

QnA WebAPP designed for questions and answers for anything

## Installation

- Create a virtual environment of your choice
- install requirements using `pip install -r requirements.txt`
- Create a database using server and driver of choice, PostgreSQL is already ready to go
- Create environment variables for `FLASK_ENV`, `DATABASE_URL`, and `SECRET_KEY`
    - `FLASK_ENV` - can either be `develop`, `production`, or `testing`
    - `DATABASE_URL` - the database URI
    - `SECRET_KEY` - The string you will be using to sign your web tokens

## Migrations

- When Database is ready, run `./manage.py db init` to create the migrations folder
- Run `./manage.py db migrate` to write the migration files
- User `./manage.py db upgrade` to write changes to database

When these steps are done you should be able to utilize the API in its entirety with Postman.  
Tokens are returned from `POST auth/login` and `POST /users/`. For authenticated routes, add header `Authorization: {token}`


## SwaggerUI

- Swagger UI is located at the base URL, defaults to `http://localhost:5000/`
