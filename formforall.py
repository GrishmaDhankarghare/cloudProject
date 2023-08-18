from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TimeField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, NumberRange
from models import Users, Venue, Show, Ticket



class Search_Form(FlaskForm):
  searched=StringField('Searched', validators=[InputRequired(message="Keyword like ratings or location is required.")])  
  
  submit_button=SubmitField('Search')
  
  
class Ticket_Form(FlaskForm):
  user_id       =IntegerField() 
  show_id       =IntegerField('Show Id')
  no_of_tickets =IntegerField('No. of Tickets', validators =[InputRequired(message = "No. of Tickets is required."), NumberRange(min=1)])
  total_price   =IntegerField('Total price', validators =[InputRequired(message = "Total Price is required."), NumberRange(min=1)])  
  
  submit_button=SubmitField('Confirm')


class Venue_Form(FlaskForm):
  v_name = StringField('Venue name', validators = [InputRequired(message = "Venue name required.")])

  location = StringField('Full Address', validators = [InputRequired(message = "Address is required."), Length(min=6, max=80, message = "Address name must be between 6 and 80 characters")])
  
  place = StringField('Building/Place')
  
  submit_button=SubmitField('Submit')


class Show_Form(FlaskForm):
  title = StringField('Show name', validators = [InputRequired(message = "Show name is required.")])

  venue = StringField('Venue name', validators = [InputRequired(message = "Venue name is required.")])
  
  timing = TimeField('Timing of the show', validators = [InputRequired(message = "Timing is required.")])
  
  day = StringField('Day of the show', validators = [InputRequired(message = "Day is required.")])
  
  rating = IntegerField('Rating')
  
  capacity = IntegerField('Total tickets', validators = [InputRequired(message = "Total tickets is required."), NumberRange(min=0, max=1000,message = "Range is 0-1000")])
  
  available_seats = IntegerField('Available Seats', validators = [InputRequired(message = "Available Seats is required."), NumberRange(min=0, max=1000,message = "Range is 0-1000")])
  
  price = IntegerField('Price per ticket', validators = [InputRequired(message = "Price is required."), NumberRange(min=0, max=1000,message = "Range is 0-1000")])
  
  submit_button=SubmitField('Submit')
  
  def validate_venue(self, venue):
    user_object = Venue.query.filter_by(v_name=venue.data).first()
    if user_object:
      pass
    else: 
      raise ValidationError("Create venue before creating a show to the venue")
  
  def validate_day(self, day):
    days=['MON', 'TUES','WEDNES','THURS','FRI','SAT','SUN']
    if self.day.data in days :
      pass
    else:
      raise ValidationError(f"Day should be from {days}")
      


def invalid_credentials(form, field):
  username_entered=form.username.data
  password_entered=field.data
  
  user_object=Users.query.filter_by(username=username_entered).first()
  if user_object is None:
    raise ValidationError("Username or Password is incorrect.")
  elif password_entered != user_object.password:
    raise ValidationError("Username or Password is incorrect.")
  

class Registration_Form(FlaskForm):
  username=StringField('Username', validators=[InputRequired(message="Username required."), Length(min=4, max=25,message="Username must be between 4 and 25 characters.")])
  
  password = PasswordField('Password', validators=[InputRequired(message="Password required.")])
  
  c_pswd=PasswordField('Cpass',validators=[InputRequired(), EqualTo('password', message="Must match with the password above.")])
  
  submit_button=SubmitField('Register')
  
  
  def validate_username(self, username):
    user_object=Users.query.filter_by(username=username.data).first()
    if user_object:
      raise ValidationError("Someone else has taken this username!Enter another username.")
  
  
class Login_Form(FlaskForm):
  username=StringField('Username', validators=[InputRequired(message="Username required."), Length(min=4, max=25,message="Username must be between 4 and 25 characters")])
  
  password = PasswordField('Password', validators=[InputRequired(message="Password required."),invalid_credentials])
  
  submit_button=SubmitField('Login')
  
