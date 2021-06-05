from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os, pymongo, random

load_dotenv()
databaseURL = os.getenv("databaseURL")
flaskKey = os.getenv("flaskKey")


webapp = Flask(__name__)

def verifyUsr(username, password):
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["accounts"]
    result = collection.find_one({"username": username.lower(), "password":password})
    if result is None:
        return False
    return True

def newUsr(username, password, confirmPassword):
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["accounts"]
    if password!=confirmPassword:
        return "The passwords do not match."
    elif collection.find_one({"username":username.lower()})!=None:
        return "That account already exists."
    collection.insert_one({"username":username.lower(), "password":password})

def fetchRandomListing():
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["listings"]
    listings=[]
    for listing in collection.find():
        listings.append(listing)
    listing = random.choice(listings)
    return listing

@webapp.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        
        valid = verifyUsr(username, password)
        if not valid:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for("index"))
    return render_template('login.html', error=error)

@webapp.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        error = newUsr(username, password, confirmPassword)
        if error==None:
            return redirect(url_for("login"))
        flash(error)
    return render_template('register.html')


@webapp.route("/home")
def index():
    listing = fetchRandomListing()
    return render_template("index.html", title=listing["title"], account=listing["account"].capitalize(), imageURL=listing["imageURL"], description=listing["description"], price=listing["price"])

@webapp.route("/listings")
def listings():
    return render_template("listings.html")

@webapp.route("/account")
def account():
    return render_template("account.html")

@webapp.route("/secret/")
def secretPage():
    return "Congratulations, you have found the secret hidden webpage that nobody knows about."

@webapp.route("/secret/<name>/")
def secretName(name):
    return f"Congratulations, {name}, you have found the secret hidden webpage that nobody knows about."

if __name__=="__main__":
    webapp.secret_key = flaskKey
    webapp.run(port=4200, debug=True)
