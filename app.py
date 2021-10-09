import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


  '''
      implement endpoint
      GET /movies
          This endpoint can be accessed by Casting Assistant, Casting Director, and Executive Producer.
          it should require the 'get:movies' permission
      returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
          or appropriate status code indicating reason for failure
  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in movies]

    return jsonify({
      'success': True,
      'movies': movies
    })


  '''
      implement endpoint
      GET /actors
          This endpoint can be accessed by Casting Assistant, Casting Director, and Executive Producer.
          it should require the 'get:actors' permission
      returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
          or appropriate status code indicating reason for failure
  '''
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    actors = [actor.format() for actor in actors]

    return jsonify({
      'success': True,
      'actors': actors
    })


  '''
      implement endpoint
      POST /movies
          This endpoint can be accessed by Executive Producer.
          it should create a new row in the movies table
          it should require the 'post:movies' permission
      returns status code 200 and json {"success": True, "movies": movie} where movies is an array containing only the newly added movies
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movie(payload):
    # Get json body from request
    body = request.get_json()
    # If request has no json body return 400
    if body is None:
      abort(400)

    # Get movie data from request's json body
    title =  body.get('title', None)
    release_date = body.get('release_date', None)

    # If movie data isn't available in the request's json body return 400
    if title is None or release_date is None:
      abort(400)

    # Proccess release_date and return 400 if not valid
    try:
      release_date = datetime.strptime(release_date, "%B %d, %Y").date()
    except:
      abort(400)

    # Add the new movie to the movies table
    movie = Movie(title=title, release_date=release_date)
    try:
      movie.insert()
      return jsonify({
        'success': True,
        'movies': [movie.format()]
      })
    except:
      abort(422)


  '''
      implement endpoint
      POST /actors
          This endpoint can be accessed by Casting Director, and Executive Producer.
          it should create a new row in the actors table
          it should require the 'post:actors' permission
      returns status code 200 and json {"success": True, "actors": actor} where actors is an array containing only the newly added actor
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actors(payload):
    # Get json body from request
    body = request.get_json()
    # If request has no json body return 400
    if body is None:
      abort(400)

    # Get actor data from request's json body
    name =  body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    # If actor data isn't available in the request's json body return 400
    if name is None or age is None or gender is None:
      abort(400)

    # Proccess gender and return 400 if not valid
    if gender == 'male':
      gender = True
    elif gender == 'female':
      gender = False
    else:
      abort(400)

    # Add the new actor to the actors table
    actor = Actor(name=name, age=age, gender=gender)
    try:
      actor.insert()
      return jsonify({
        'success': True,
        'actors': [actor.format()]
      })
    except:
      abort(422)


  '''
      implement endpoint
      PATCH /movies/<id>
          where <id> is the existing model id
          This endpoint can be accessed by Casting Director, and Executive Producer.
          it should respond with a 404 error if <id> is not found
          it should update the corresponding row for <id>
          it should require the 'patch:movies' permission
      returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
          or appropriate status code indicating reason for failure
  '''
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    # Query database for required movie
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    # Get the request's json body and verify its data
    body = request.get_json()
    if body is None:
      abort(400)

    title = body.get('title', None)
    release_date = body.get('release_date', None)

    if title is None and release_date is None:
      abort(400)

    # Update the movie's title
    if title is not None:
      movie.title = title
    
    # Update the movie's release date
    if release_date is not None:
      # Proccess release_date and return 400 if not valid
      try:
        movie.release_date = datetime.strptime(release_date, "%B %d, %Y").date()
      except:
        abort(400)

    # Commit updates to database
    try:
      movie.update()

      return jsonify({
        'success': True,
        'movies': [movie.format()]
      })
    except:
      abort(422)


  '''
      implement endpoint
      PATCH /actor/<id>
          where <id> is the existing model id
          This endpoint can be accessed by Casting Director, and Executive Producer.
          it should respond with a 404 error if <id> is not found
          it should update the corresponding row for <id>
          it should require the 'patch:actors' permission
      returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
          or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    # Query database for required movie
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    # Get the request's json body and verify its data
    body = request.get_json()
    if body is None:
      abort(400)

    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    if name is None and age is None and gender is None:
      abort(400)

    # Update the actor's name
    if name is not None:
      actor.name = name

    # Update the actor's age
    if age is not None:
      actor.age = age
    
    # Update the actor's gender
    if gender is not None:
      if gender == 'male':
        actor.gender = True
      elif gender == 'female':
        actor.gender = False
      else:
        abort(400)

    # Commit updates to database
    try:
      actor.update()

      return jsonify({
        'success': True,
        'actors': [actor.format()]
      })
    except:
      abort(422)

  '''
      implement endpoint
      DELETE /movies/<id>
          where <id> is the existing model id
          This endpoint can be accessed by Executive Producer.
          it should respond with a 404 error if <id> is not found
          it should delete the corresponding row for <id>
          it should require the 'delete:movies' permission
      returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
          or appropriate status code indicating reason for failure
  '''
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    # Query database for required movie
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    # Delete the row from the database
    try:
      movie.delete()

      return jsonify({
        'success': True,
        'delete': movie_id
      })
    except:
      abort(422)


  '''
      implement endpoint
      DELETE /actors/<id>
          where <id> is the existing model id
          This endpoint can be accessed by Casting Director, and Executive Producer.
          it should respond with a 404 error if <id> is not found
          it should delete the corresponding row for <id>
          it should require the 'delete:movies' permission
      returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
          or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    # Query database for required movie
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    # Delete the row from the database
    try:
      actor.delete()

      return jsonify({
        'success': True,
        'delete': actor_id
      })
    except:
      abort(422)


  # Error Handling
  '''
      implement error handler for 422
  '''
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422


  '''
      implement error handler for 400
  '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False, 
          "error": 400,
          "message": "bad request"
          }), 400


  '''
      implement error handler for 404
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "resource not found"
          }), 404

  '''
      implement error handler for AuthError
  '''
  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)