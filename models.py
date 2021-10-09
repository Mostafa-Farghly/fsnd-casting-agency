import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
# Fix for heroku 'postgresql' instead of 'postgres'
if database_path[0:8] == 'postgres':
  if database_path[8:10] != 'ql':
    database_path = database_path[:8]+'ql' + database_path[8:]

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movies
Have title and release date
'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(db.Integer, primary_key=True)
  title = Column(db.String(), nullable=False)
  release_date = Column(db.Date, nullable=False)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date.strftime('%B %d, %Y')
    }


'''
Actors 
Have name, age and gender
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String(), nullable=False)
  age = Column(db.Integer, nullable=False)
  gender = Column(db.Boolean, nullable=False)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': 'male' if self.gender else 'female'
    }