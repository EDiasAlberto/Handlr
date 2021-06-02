from flask import Flask as fl
from flask import render_template
import os

webapp = fl(__name__)

@webapp.route("/")
def index():
    return render_template("login.html")

@webapp.route("/home")
def home():
    return render_template("index.html")

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
    webapp.run(port=4200, debug=True)
