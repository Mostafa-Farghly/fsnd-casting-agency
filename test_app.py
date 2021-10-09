import os
import unittest
import json
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """
    This class represents the casting agency test case
    Before starting the test make sure to run the following commands to initialize the database:
    --> $ dropdb -U postgres capstone_test
    --> $ createdb -U postgres capstone_test
    --> $ psql -U postgres capstone_test < casting_agency.psql
    Then run the tests by running:
    --> $ python3 test_app.py
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        # Fix for 'postgresql' instead of 'postgres'
        if self.database_path[0:8] == 'postgres':
            if self.database_path[8:10] != 'ql':
                self.database_path = self.database_path[:8]+'ql' + self.database_path[8:]
        setup_db(self.app, self.database_path)

        # Movie to be inserted to database
        self.new_movie = {
            'title': 'No Time To Die',
            'release_date': 'October 7, 2021'
        }

        # Actor to be inserted to database
        self.new_actor = {
            'name': 'Daniel Craig',
            'age': 53,
            'gender': 'male'
        }
        
        # Empty JSON to test bad request
        self.empty_json = {}

        # Access tokens
        self.executive_producer_token = os.environ['EXECUTIVE_PRODUCER_TOKEN']
        self.casting_director_token = os.environ['CASTING_DIRECTOR_TOKEN']
        self.casting_assistant_token = os.environ['CASTING_ASSISTANT_TOKEN']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    

    def tearDown(self):
        """Executed after reach test"""
        pass

    
    def test_get_movies_casting_assistant_role(self):
        """
        GET request for '/movies' endpoint should return a list of
        movies.
        It requires 'get:movies' permission.
        Cassting Assistant role is used to make request.
        """
        res = self.client().get(
            '/movies',
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(isinstance(data['movies'], list))


    def test_401_get_movies_without_token(self):
        """
        GET request for '/movies' endpoint requires 'get:movies' permission 
        """
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Authorization header is expected.')

    
    def test_get_actors_casting_assistant_role(self):
        """
        GET request for '/actors' endpoint should return a list of
        actors.
        It requires 'get:actors' permission.
        Cassting Assistant role is used to make request.
        """
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(isinstance(data['actors'], list))


    def test_401_get_actors_without_token(self):
        """
        GET request for '/actors' endpoint requires 'get:actors' permission 
        """
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Authorization header is expected.')


    def test_post_movies_executive_producer_role(self):
        """
        POST request for '/movies' endpoint should return a list of
        movies with only the movie added.
        It requires 'post:movies' permission.
        Executive Producer role is used to make request.
        """
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(isinstance(data['movies'], list))
        self.assertEqual(len(data['movies']), 1)
        self.assertEqual(data['movies'][0]['title'], 'No Time To Die')
        self.assertEqual(data['movies'][0]['release_date'], 'October 07, 2021')
        self.assertTrue(data['movies'][0]['id'])



    def test_403_post_movies_casting_assistant_role(self):
        """
        POST request for '/movies' endpoint requires 'post:movies' permission.
        Casting Assistant doesn't have the required permission.
        """
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Permission not found')


    def test_400_post_movies_empty_json(self):
        """
        POST request for '/movies' endpoint requires 'post:movies' permission.
        Executive producer role is used to make request.
        It should return bad request 400 because of empty json in request body.
        """
        res = self.client().post(
            '/movies',
            json=self.empty_json,
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')


    def test_post_actors_casting_director_role(self):
        """
        POST request for '/actors' endpoint should return a list of
        actors with only the actor added.
        It requires 'post:actors' permission.
        Casting Director role is used to make request.
        """
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={
                'Authorization': 'Bearer ' + self.casting_director_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(isinstance(data['actors'], list))
        self.assertEqual(len(data['actors']), 1)
        self.assertEqual(data['actors'][0]['name'], 'Daniel Craig')
        self.assertEqual(data['actors'][0]['age'], 53)
        self.assertEqual(data['actors'][0]['gender'], 'male')
        self.assertTrue(data['actors'][0]['id'])



    def test_403_post_actors_casting_assistant_role(self):
        """
        POST request for '/actors' endpoint requires 'post:movies' permission.
        Casting Assistant doesn't have the required permission.
        """
        res = self.client().post(
            '/actors',
            json=self.new_movie,
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Permission not found')

    
    def test_400_post_actors_empty_json(self):
        """
        POST request for '/actors' endpoint requires 'post:actors' permission.
        Executive producer role is used to make request.
        It should return bad request 400 because of empty json in request body.
        """
        res = self.client().post(
            '/actors',
            json=self.empty_json,
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')


    def test_patch_movies_executive_producer_role(self):
        """
        PACTH request for '/movies/<int:movie_id>' endpoint should return a list of movies with only the updated movie.
        It requires 'patch:movies' permission.
        Executive Producer role is used to make request.
        """
        res = self.client().patch(
            '/movies/1',
            json={
                'title': 'The Batman',
                'release_date': 'March 04, 2022'
            },
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(isinstance(data['movies'], list))
        self.assertEqual(len(data['movies']), 1)
        self.assertEqual(data['movies'][0]['title'], 'The Batman')
        self.assertEqual(data['movies'][0]['release_date'], 'March 04, 2022')
        self.assertEqual(data['movies'][0]['id'], 1)



    def test_403_patch_movies_casting_assistant_role(self):
        """
        PATCH request for '/movies/<int:movie_id>' endpoint requires 'patch:movies' permission.
        Casting Assistant doesn't have the required permission.
        """
        res = self.client().patch(
            '/movies/1',
            json={
                'title': 'The Batman',
                'release_date': 'March 04, 2022'
            },
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Permission not found')


    def test_400_patch_movies_empty_json(self):
        """
        PACTH request for '/movies/<int:movie_id>' endpoint requires 'pacth:movies' permission.
        Executive producer role is used to make request.
        It should return bad request 400 because of empty json in request body.
        """
        res = self.client().patch(
            '/movies/1',
            json=self.empty_json,
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')


    def test_404_patch_movies_nonexistant_id(self):
        """
        PACTH request for '/movies/<int:movie_id>' endpoint requires 'patch:movies' permission.
        Executive producer role is used to make request.
        It should return not found 404 because of movie_id=1000 not found.
        """
        res = self.client().patch(
            '/movies/1000',
            json={
                'title': 'The Batman',
                'release_date': 'March 04, 2022'
            },
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_patch_actors_executive_producer_role(self):
        """
        PACTH request for '/actors/<int:actor_id>' endpoint should return a list of actors with only the updated actor.
        It requires 'patch:actors' permission.
        Executive Producer role is used to make request.
        """
        res = self.client().patch(
            '/actors/1',
            json={
                'name': 'Tom Holland',
                'age': 25,
                'gender': 'male'
            },
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(isinstance(data['actors'], list))
        self.assertEqual(len(data['actors']), 1)
        self.assertEqual(data['actors'][0]['name'], 'Tom Holland')
        self.assertEqual(data['actors'][0]['age'], 25)
        self.assertEqual(data['actors'][0]['gender'], 'male')
        self.assertEqual(data['actors'][0]['id'], 1)



    def test_403_patch_actors_casting_assistant_role(self):
        """
        PATCH request for '/actors/<int:actor_id>' endpoint requires 'patch:actors' permission.
        Casting Assistant doesn't have the required permission.
        """
        res = self.client().patch(
            '/actors/1',
            json={
                'name': 'Tom Holland',
                'age': 25,
                'gender': 'male'
            },
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Permission not found')


    def test_400_patch_actors_empty_json(self):
        """
        PACTH request for '/actors/<int:actor_id>' endpoint requires 'patch:actors' permission.
        Executive producer role is used to make request.
        It should return bad request 400 because of empty json in request body.
        """
        res = self.client().patch(
            '/actors/1',
            json=self.empty_json,
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')


    def test_404_patch_actors_nonexistant_id(self):
        """
        PACTH request for '/actors/<int:actors_id>' endpoint requires 'patch:actors' permission.
        Executive producer role is used to make request.
        It should return not found 404 because of actor_id=1000 not found.
        """
        res = self.client().patch(
            '/actors/1000',
            json={
                'name': 'Tom Holland',
                'age': 25,
                'gender': 'male'
            },
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_403_delete_movies_casting_director_role(self):
        """
        DELETE request for '/movies/<int:movie_id>' endpoint requires 'delete:movies' permission.
        Casting Director doesn't have the required permission.
        """
        res = self.client().delete(
            '/movies/2',
            headers={
                'Authorization': 'Bearer ' + self.casting_director_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Permission not found')


    def test_403_delete_movies_casting_assistant_role(self):
        """
        DELETE request for '/movies/<int:movie_id>' endpoint requires 'delete:movies' permission.
        Casting Assistant doesn't have the required permission.
        """
        res = self.client().delete(
            '/movies/2',
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Permission not found')


    def test_404_delete_movies_nonexistant_id(self):
        """
        DELETE request for '/movies/<int:movie_id>' endpoint requires 'delete:movies' permission.
        Executive producer role is used to make request.
        It should return not found 404 because of movie_id=1000 not found.
        """
        res = self.client().delete(
            '/movies/1000',
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_movies_executive_producer_role(self):
        """
        DELETE request for '/movies/<int:movie_id>' endpoint should return the id of the deleted movie.
        It requires 'delete:movies' permission.
        Executive Producer role is used to make request.
        """
        res = self.client().delete(
            '/movies/2',
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)


    def test_403_delete_actors_casting_assistant_role(self):
        """
        DELETE request for '/actors/<int:actor_id>' endpoint requires 'delete:actors' permission.
        Casting Assistant doesn't have the required permission.
        """
        res = self.client().delete(
            '/actors/2',
            headers={
                'Authorization': 'Bearer ' + self.casting_assistant_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])
        self.assertEqual(data['description'], 'Permission not found')


    def test_404_delete_actors_nonexistant_id(self):
        """
        DELETE request for '/actors/<int:actor_id>' endpoint requires 'delete:actors' permission.
        Executive producer role is used to make request.
        It should return not found 404 because of movie_id=1000 not found.
        """
        res = self.client().delete(
            '/actors/1000',
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_actors_casting_director_role(self):
        """
        DELETE request for '/actors/<int:actor_id>' endpoint should return the id of the deleted dirctor.
        It requires 'delete:actors' permission.
        Casting Director role is used to make request.
        """
        res = self.client().delete(
            '/actors/2',
            headers={
                'Authorization': 'Bearer ' + self.executive_producer_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
