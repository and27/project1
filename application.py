import os

from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from wrapd import loginRequired

import requests

app = Flask(__name__)


app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@loginRequired
def index():
        return render_template("index.html",)

@app.route("/signin", methods=['POST','GET'])
def signin():
	#Forget any username
	session.clear()

	username = request.form.get("username")
	pwd = request.form.get("pwd")

	if request.method == "POST":
		if not username:
			return render_template("error.html", message="Enter a valid user")		
	
		if not pwd:
			return render_template("error.html", message="Please provide a password")

		users = db.execute("SELECT * FROM users WHERE username = :username", {"username":username})
		result = users.fetchone()

		if result == None or not check_password_hash(result[2], pwd):
			return render_template("error.html", message="invalid username or password")
				
		session["user_id"]=result[0]
		session["user_name"]=result[1]

		#Redirect to home page where you can search for books
		return redirect("/")
	else:
		return render_template("signin.html")



@app.route("/register", methods=['POST','GET'])
def register():
	
	session.clear()
	username=request.form.get("username")
	email=request.form.get("email")
	pwd=request.form.get("pwd")
	

	if request.method=="POST":
		
		if len(username) <1 or username is '':
			return render_template("error.html", message="Please enter a username")
	
		elif len(pwd) <1 or pwd is '':
			return render_template("error.html", message="Please enter a password")

		elif not email:
			return render_template("error.html", message="Please enter an email")
		

		hashedPwd = generate_password_hash(pwd)

		db.execute("INSERT INTO users (username, email, pwd) VALUES (:username, :email, :hash)",
		{"username": username, "email":email, "hash":hashedPwd})
		db.commit()
		

		return redirect("/signin")
	else:
		return render_template("register.html")
	
	
	
@app.route("/logout", methods=['GET'])
def logout():
        try:
                usersLogged.remove(session['username'])
        except ValueError:
                pass

        session.clear()
        return redirect("/")

@app.route("/book")
def book():
	key = os.getenv("GK")
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "zgCIPXS2iExBycqVhbczPA", "isbns": "9781632168146"})
	print(res.json())


