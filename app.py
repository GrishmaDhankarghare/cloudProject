from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from formforall import *
from models import *

#configure app
app = Flask(__name__)
app.secret_key = "reload"

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GYT.db'
db.init_app(app)
app.app_context().push()

#configure flask login
login = LoginManager(app)
login.login_view = "/login"

@app.route("/", methods = ['GET','POST'])
def index():
  return render_template("index.html", venues = Venue.query.all(),shows = Show.query.all())
    
  
@app.route("/admin", methods = ['GET','POST'])
def ad_login():
  log_form      =Login_Form()
  if log_form.validate_on_submit():
    user_object =Users.query.filter_by(username = log_form.username.data).first()
    login_user(user_object)
    return redirect(url_for("venues"))
  return render_template("ad_login.html", form = log_form)
  

@app.route("/venues",methods = ['GET', 'POST']) 
def venues():
  if not current_user.is_authenticated or current_user.role != "admin":
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  return render_template("venues.html",venues = Venue.query.all(), shows = Show.query.all())
  
  
@app.route("/venue/edit/<int:id>", methods = ['GET','POST'])  
def edit_venue(id):
  if not current_user.is_authenticated or current_user.role != "admin" :
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  venue                    =Venue.query.get_or_404(id)
  venue_form               =Venue_Form()
  if venue_form.validate_on_submit():
    venue.v_name           =venue_form.v_name.data
    venue.location         =venue_form.location.data
    venue.place            =venue_form.place.data
    venue.verified         =True
    db.session.commit()
    flash('Venue edited successfully.','success')
    return redirect(url_for('venues'))
  venue_form.v_name.data   =venue.v_name
  venue_form.location.data =venue.location
  venue_form.place.data    =venue.place
  return render_template("edit_venue.html", form = venue_form,id = id)
  
  
@app.route("/venue/delete/<int:id>")  
def delete_venue(id):
  if not current_user.is_authenticated or current_user.role != "admin":
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  venue=Venue.query.get_or_404(id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted successfully.','success')
    return redirect(url_for('venues'))
  except:
    flash("There's a problem. Try again.")
    return redirect(url_for('venues'))
    
    
@app.route("/new venue", methods = ['GET','POST'])
def venue():
  if not current_user.is_authenticated or current_user.role != "admin":
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  venue_form =Venue_Form()
  if venue_form.validate_on_submit():
    v_name   =venue_form.v_name.data
    location =venue_form.location.data
    place    =venue_form.place.data
    
    venue    =Venue(v_name = v_name, location = location, place = place)  
    db.session.add(venue)
    db.session.commit()
    flash('Venue added successfully.','success')
    return redirect(url_for('venues'))
  return render_template("new_venue.html", form = venue_form)
  
  
@app.route("/new show/<int:id>", methods = ['GET','POST'])
def show(id):
  if not current_user.is_authenticated or current_user.role != "admin":
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  v                 =Venue.query.get_or_404(id)
  show_form         =Show_Form()
  if show_form.validate_on_submit():
    title           =show_form.title.data
    timing          =show_form.timing.data
    venue           =show_form.venue.data
    day             =show_form.day.data
    rating          =show_form.rating.data
    capacity        =show_form.capacity.data
    available_seats =show_form.available_seats.data
    price           =show_form.price.data
    
    show            =Show(title = title, venue = venue, timing = timing, day = day, rating = rating, capacity = capacity, price = price, available_seats = available_seats)
    db.session.add(show)
    db.session.commit()
    flash('Show added successfully.','success')
    return redirect(url_for('venues'))
  show_form.venue.data = v.v_name  
  return render_template("new_show.html", form = show_form, id = id)
  
  
@app.route("/show/<int:id>", methods = ['GET','POST'])  
def view_show(id):
  if not current_user.is_authenticated or current_user.role != "admin":
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  show=Show.query.get_or_404(id) 
  return render_template("show.html", show = show) 
  
  
@app.route("/show/edit/<int:id>", methods = ['GET','POST'])  
def edit_show(id):
  if not current_user.is_authenticated or current_user.role != "admin":
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  show                   =Show.query.get_or_404(id)
  show_form              =Show_Form()
  if show_form.validate_on_submit():
    show.title           =show_form.title.data
    show.timing          =show_form.timing.data
    show.day             =show_form.day.data
    show.venue           =show_form.venue.data
    show.rating          =show_form.rating.data
    show.capacity        =show_form.capacity.data
    show.available_seats =show_form.available_seats.data
    show.price           =show_form.price.data
    show.verified        =True
    db.session.commit()
    flash('Show edited successfully.','success')
    return redirect(url_for('view_show',id = id))
  show_form.title.data           =show.title
  show_form.venue.data           =show.venue
  show_form.timing.data          =show.timing
  show_form.day.data             =show.day
  show_form.capacity.data        =show.capacity
  show_form.available_seats.data =show.available_seats
  show_form.rating.data          =show.rating
  show_form.price.data           =show.price
  return render_template("edit_show.html", form = show_form, id = id)
  
  
@app.route("/show/delete/<int:id>") 
def delete_show(id):
  if not current_user.is_authenticated or current_user.role != "admin":
    flash('Please login as an admin.','danger')
    return redirect(url_for('ad_login'))
  show = Show.query.get_or_404(id)
  try:
    db.session.delete(show)
    db.session.commit()
    flash('Venue deleted successfully.','success')
    return redirect(url_for('venues'))
  except:
    flash("There's a problem. Try again.")
    return redirect(url_for('venues'))
  
  
@app.route("/ad_logout",methods = ['GET'])
def ad_logout():
  logout_user()
  flash('Admin have logout successfully.','success')
  return redirect(url_for('index'))


@app.context_processor
def home():
  search_form      =Search_Form()
  return dict(form =search_form)  
  
@app.route("/search", methods = ['POST'])  
def search():
  search_form     = Search_Form()
  
  if search_form.validate_on_submit():
    show_results  = Show.query
    searched      = search_form.searched.data
    show_results  = show_results.filter(Show.title.like('%' + searched + '%'))
    show_results  = show_results.order_by(Show.title).all()
    venue_results = Show.query
    venue_results = venue_results.filter(Show.venue.like('%' + searched + '%'))
    venue_results = venue_results.order_by(Show.title).all()
    return render_template("search.html", form = search_form, searched = searched, results = show_results+venue_results)
    

@login.user_loader
def load_user(id):
  return Users.query.get(id) 
  
@app.route("/login", methods = ['GET','POST'])
def login():
  log_form      =Login_Form()
  if log_form.validate_on_submit():
    user_object =Users.query.filter_by(username = log_form.username.data).first()
    login_user(user_object)
    return redirect(url_for("index"))
  return render_template("login.html", form = log_form)  
  

@app.route("/book_tickets/<int:id>", methods = ['GET','POST'])   
def booking(id):
  if not current_user.is_authenticated or current_user.role == "admin":
    flash('Please login as a user.','danger')
    return redirect(url_for('login'))
  show = Show.query.get_or_404(id)
  if show.available_seats == 0:
    flash ("Housefull, can't book tickets for this show.")
  else:
    ticket_form         =Ticket_Form()
    if ticket_form.validate_on_submit():
      no_of_tickets     =ticket_form.no_of_tickets.data
      total_price       =ticket_form.total_price.data
      if (no_of_tickets > show.available_seats) or ( total_price != show.price * no_of_tickets):
        flash ("Please fill appropriately")
        return render_template("booking.html", form = ticket_form, show = show, id = id)
      ticket            =Ticket(user_id = current_user.id, show_id = show.id, no_of_tickets = no_of_tickets, total_price = total_price)
      db.session.add(ticket)
      show.available_seats =show.available_seats - no_of_tickets
      db.session.commit()
      flash ("Tickets book successfully")
      return render_template("tickets.html", tickets = Ticket.query.all(), shows = Show.query.all(), id = current_user.id)
    return render_template("booking.html", form = ticket_form, show = show, id = id)  
  return render_template("index.html", venues = Venue.query.all(),shows = Show.query.all())
    
   
@app.route("/tickets", methods = ['GET','POST'])
def tickets():
  if not current_user.is_authenticated or current_user.role == "admin":
    flash('Please login as a user.','danger')
    return redirect(url_for('login'))
  return render_template("tickets.html", tickets = Ticket.query.all(), shows = Show.query.all(), id = current_user.id)      
  
   
@app.route("/logout",methods = ['GET'])
def logout():
  logout_user()
  flash('You have logout successfully.','success')
  return redirect(url_for('login'))
 
 
@app.route("/new user", methods = ['GET','POST'])
def register():
  reg_form   =Registration_Form()
  if reg_form.validate_on_submit():
    username =reg_form.username.data
    password =reg_form.password.data
    
    user     =Users(username=username,password=password)
    db.session.add(user)
    db.session.commit()
    flash('Register successfully. Please login.','success')
    return redirect(url_for('login'))
    
  return render_template("new_user.html", form = reg_form)
  

if __name__ == '__main__':
  app.debug=True
  app.run()
  
