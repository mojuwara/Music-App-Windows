from flask import Flask, render_template, request, redirect, session, url_for, g
from flask_cors import CORS
from scrape_songs import *
from models import *
import os 
import random

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(random.randint(1, 32))

# Upon entry, take them to a page to log in or register
@app.route("/", methods=["GET"])
def entry():
  return render_template("index.html")

# Direct to the log in page
@app.route("/log-in", methods=["GET"])
def login():
  return render_template("login.html")

# Direct user to the register page
@app.route("/register", methods=["GET"])
def register():
  return render_template("register.html")

# Removes the current user from session and redirects to login page
@app.route("/log-out")
def log_out():
  session.pop("user", None)
  return render_template("index.html")

# Check if the log in credentials are in the database
@app.route("/login_auth", methods=["POST"])
def login_auth():
  session.pop("user", None)
  username = request.form["username"]
  password = request.form["password"]
  if (is_user(username, password)):
    session["user"] = username
    return render_template("profile.html", name=username)

  error = "There is no account with this username/password combination."
  return render_template("login.html", error=error)

@app.route("/profile")
def profile():
  if ("user" not in session):
    return render_template("index.html")

  return render_template("profile.html", name=session["user"])

# Check if the username is available
@app.route("/register_auth", methods=["POST"])
def register_auth():
  username = request.form["username"]
  password = request.form["password"]
  if (is_now_registered(username, password)):
    session["user"] = username
    return render_template("profile.html", name=session["user"])

  error = "The username '{}' is already taken.".format(username)
  return render_template("register.html", error=error)

# User can add new artists to view music from
@app.route("/add-artists", methods=["POST", "GET"])
def add_artists():
  if ("user" not in session):
    return render_template("index.html")

  if (request.method == "GET"): # Get artists not already liked by user
    new_artists = search_neutral_artists(session["user"])
    return render_template("add-artists.html", artists=new_artists)
  
  if (request.method == "POST"):
    selected_artists = request.form.getlist("Artists")
    store_new_artists(session["user"], selected_artists)
    return render_template("profile.html", name=session["user"])

# Returns a list of songs with people the user "likes" (from newest to oldest)
@app.route("/new-music")
def new_music():
  if ("user" not in session): 
    return render_template("index.html")

  songs_list = search_new_songs(session["user"])
  return render_template("new-music.html", songs=songs_list)

# Remove artists that you don't want to listen to
@app.route("/dislike-artists", methods=["GET", "POST"])
def dislike_artists():
  if ("user" not in session):
    return render_template("index.html")

  elif (request.method == "GET"):
    neutral_artists = search_neutral_artists(session["user"])
    return render_template("dislike-artists.html", artists=neutral_artists)

  else: #(request.method == "POST"):
    disliked = request.form.getlist("Artists")
    dislike(session["user"], disliked)
    return render_template("profile.html", name=session["user"])

# Remove artists from the Like table
@app.route("/remove-artists", methods=["GET", "POST"])
def remove_artists():
  if "user" not in session:
    return render_template("index.html")

  elif request.method == "GET":
    liked_artists = get_liked_artists(session["user"])
    return render_template("remove-artists.html", artists=liked_artists)

  else:
    artists = request.form.getlist("Artists")
    remove_from_liked(session["user"], artists)
    return render_template("/profile.html", name=session["user"])

# Remove artists from the Dislike table
@app.route("/show-again", methods=["GET", "POST"])
def show_again():
  if "user" not in session:
    return render_template("index.html")

  elif request.method == "GET":
    disliked_artists = get_disliked_artists(session["user"])
    return render_template("show-again.html", artists=disliked_artists)

  else:
    show_again = request.form.getlist("Artists")
    remove_from_disliked(session["user"], show_again)
    return render_template("profile.html", name=session["user"])

if __name__ == "__main__":
  # Start up MAMP
  os.system("cd ../../; cd /Applications/MAMP/bin && ./start.sh")
  app.run(debug=True)