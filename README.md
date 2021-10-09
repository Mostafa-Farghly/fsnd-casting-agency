# FSND Capstone Project (Casting Agency)


## Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This project creates a system to simplify and streamline the process.
The app is hosted on [Heroku](https://www.heroku.com/platform) at `https://mostafa-casting-agency.herokuapp.com/`

## Getting Started

### Pre-requisites and Local Development

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine.

Developers using this project should already have Python3, and pip installed on their local machines.

### Installing Dependencies

1. **Python 3.6.9** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - Working within a virtual environment whenever using Python for projects is recommended. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by navigating to the project directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used in this project to handle the Postgesql database.

 - [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Database Setup

#### Step 0: Start/Stop the PostgreSQL server
Mac users can follow the commands below:
```bash
which postgres
postgres --version
# Start/stop
pg_ctl -D /usr/local/var/postgres start
pg_ctl -D /usr/local/var/postgres stop 
```
Windows users can follow the commands below:
- Find the database directory, it should be something like that: *C:\Program Files\PostgreSQL\13.2\data*
- Then, in the command line, execute the folllowing command: 
```bash
# Start the server
pg_ctl -D "C:\Program Files\PostgreSQL\13.2\data" start
# Stop the server
pg_ctl -D "C:\Program Files\PostgreSQL\13.2\data" stop
```

#### Step 1 - Create and Populate the database

1. **Create the database and a user**<br>
In your terminal, run the following to create two databases:
```bash
# Create database used in development
createdb -U postgres casting_agency
# Create database used in testing
createdb -U postgres casting_agency_test
```

2. **Create tables**<br>
Once your databases are created, you can create tables (`movies`, `actors`) and apply contraints
```bash
psql -U postgres casting_agency < casting_agency.psql
```

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:movies`
   - `get:actors`
   - `post:movies`
   - `post:actors`
   - `patch:movies`
   - `patch:actors`
   - `delete:movies`
   - `delete:actors`
6. Create new roles for:
   - Casting Assistant
     - can `get:movies`, `get:actors`.
   - Casting Director
     - can perform all actions a Casting Assistant can.
     - can `post:actors`, `delete:actors`.
     - can `patch:movies`, `patch:actors`.
   - Executive Producer
     - can perform all actions

### Enivronment variables

Example is provided in the `.env.example` file.

You will need to set the following environment variables:
1. `DATABASE_URL`: The url of the database. ex: "postgresql://<user>:<password>@<url>:<port>/<database_name>"
2. `AUTH0_DOMAIN`: The appliaction's domain on Auth0.
3. `API_AUDIENCE`: The API audience used by Auth0.
Environmet variables used by test_app.py:
4. `TEST_DATABASE_URL`: The url of the database. ex: "postgresql://<user>:<password>@<url>:<port>/<database_name>"
5. `EXECUTIVE_PRODUCER_TOKEN`: JWT token of an user with an `Executive Producer` role.
6. `CASTING_DIRECTOR_TOKEN`: JWT token of an user with a `Casting Director` role.
7. `CASTING_ASSISTANT_TOKEN`: JWT token of an user with a `Casting Assistant` role.

### Running the server

From within the project directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Testing

Before running the tests make sure to set the required environment variables (Check the `Environment Variables` section).
To run the tests, run
```
dropdb -U postgres casting_agency_test
createdb -U postgres casting_agency_test
psql -U postgres casting_agency_test < casting_agency.psql
python3 test_app.py
```

## API Refrence

### Getting Started
- Base URL: The app is hosted at `https://mostafa-casting-agency.herokuapp.com/` 
- Authentication: This version of the application require authentication. When logging in to `https://dev-weuazke8.us.auth0.com/authorize?audience=castingagency&response_type=token&client_id=Hk1Bul95ANqkTxKNcvwqLhOowYYvG6WJ&redirect_uri=https://127.0.0.1:8080/login-results`, the token can be used to access the api, as it has the required permission based on the user's role.

### Error Handling
Errors are returned as JSON objects in the following format:
```js
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
Authentication errors are returned in the following format:
```js
{
    "code": "Forbidden",
    "description": "Permission not found"
}
```

The API will return five error types when requests fail:
- 400: Bad Request
- 401: unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

```js
Endpoints
GET /movies
GET /actors
DELETE /movies/{movie_id}
DELETE /actors/{actor_id}
POST /movies
POST /actors
PATCH /movies/{movie_id}
PATCH /actors/{actor_id}
```

```js
GET '/movies'
- Fetches a list of movies
- Required Permissions: `get:movies`
- Request Arguments: None
- Returns: An object with success value, and list movies, that contains an object of id: movie_id,  title: movie_title, and release_date: movie_release_date. 
{
    "movies": [
        {
            "id": 1,
            "release_date": "March 04, 2022",
            "title": "The Batman"
        },
        {
            "id": 3,
            "release_date": "October 07, 2021",
            "title": "No Time To Die"
        }
    ],
    "success": true
}
```

```js
GET '/actors'
- Fetches a list of actors
- Required Permissions: `get:actors`
- Request Arguments: None
- Returns: An object with success value, and list actors, that contains an object of id: actor_id,  name: actor_name, age: actor_age, and gender: 'male' or 'female'. 
{
    "actors": [
        {
            "age": 53,
            "gender": "Male",
            "id": 1,
            "name": "Daniel Craig"
        },
        {
            "age": 25,
            "gender": "Male",
            "id": 2,
            "name": "Tom Holland"
        }
    ],
    "success": true
}
```

```js
DELETE '/movies/${id}'
- Deletes a specified movie using the id of the movie
- Required Permissions: `delete:movies`
- Request Arguments: id - integer
- Returns: An object with success value, and the id of the deleted movie.
{
    "delete": 4,
    "success": true
}
```

```js
DELETE '/actors/${id}'
- Deletes a specified actor using the id of the actor
- Required Permissions: `delete:actors`
- Request Arguments: id - integer
- Returns: An object with success value, and the id of the deleted actor.
{
    "delete": 4,
    "success": true
}
```

```js
POST '/movies'
- Adds a new movie to the database
- Required Permissions: `post:movies`
- Request Body: 
{
    "title": "The Batman",
    "release_date": "March 4, 2022"
}
- Returns: success value, and an array containing a single new movie object 
{
    "movies": [
        {
            "id": 4,
            "release_date": "March 04, 2022",
            "title": "The Batman"
        }
    ],
    "success": true
}
```

```js
POST '/actors'
- Adds a new actor to the database
- Required Permissions: `post:actors`
- Request Body: 
{
    "name": "Tom Holland",
    "age": 25,
    "gender": "male"
}
- Returns: success value, and an array containing a single new actor object 
{
    "actors": [
        {
            "age": 25,
            "gender": "male",
            "id": 2,
            "name": "Tom Holland"
        }
    ],
    "success": true
}
```

```js
PATCH '/movies/${id}'
- Updates a specified movie using the id of the movie
- Required Permissions: `patch:movies`
- Request Arguments: id - integer
- Request Body: The body can contain only one of the title or the release_date, or it can contain both
{
    "title": "The Batman 2",
    "release_date": "March 4, 2023"
}
- Returns: success value, and an array containing a single updated movie object.
{
    "movies": [
        {
            "id": 4,
            "release_date": "March 04, 2023",
            "title": "The Batman 2"
        }
    ],
    "success": true
}
```

```js
PATCH '/actors/${id}'
- Updates a specified actor using the id of the actor
- Required Permissions: `patch:actors`
- Request Arguments: id - integer
- Request Body: The body can contain any of the name, age, or gender, or can contain all three together
{
    "name": "Tom Holland Spider Man",
    "age": 25,
    "gender": "male"
}
- Returns: An object with success value, and the id of the deleted actor.
{
    "actors": [
        {
            "age": 25,
            "gender": "male",
            "id": 2,
            "name": "Tom Holland Spider Man"
        }
    ],
    "success": true
}
```

## Authors
Mostafa Alaa

## Acknowledgements 
The awesome team at Udacity.