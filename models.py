from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db=SQLAlchemy()

class Users(UserMixin, db.Model):
  id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String(25), unique=True, nullable=False)
  password=db.Column(db.String(25), nullable=False)
  role=db.Column(db.String(10))
  
class Venue(UserMixin, db.Model):
  id=db.Column(db.Integer,primary_key=True)
  v_name=db.Column(db.String(25), unique=True, nullable=False)
  location=db.Column(db.String(80), nullable=False)
  place=db.Column(db.String())
  
class Show(UserMixin, db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String(25), nullable=False)
  venue=db.Column(db.String(25), nullable=False)  
  timing=db.Column(db.Time("%I:%M,%p"), nullable=False)
  day=db.Column(db.String(25), nullable=False)
  rating=db.Column(db.Integer)
  capacity=db.Column(db.Integer, nullable=False)
  available_seats=db.Column(db.Integer, nullable=False)
  price=db.Column(db.Integer, nullable=False)
 
class Ticket(UserMixin, db.Model):
  id=db.Column(db.Integer,primary_key=True)
  user_id=db.Column(db.Integer, nullable=False)
  show_id=db.Column(db.Integer, nullable=False)
  no_of_tickets=db.Column(db.Integer, nullable=False)  
  total_price=db.Column(db.Integer, nullable=False) 
   
   
