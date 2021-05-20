from flask import Flask as fl
import os

webapp = fl(__name__)

@webapp.route("/")
def launchPage():
    return "127.0.0.1"

@webapp.route("/secret/")
def secretPage():
    return "Congratulations, you have found the secret hidden webpage that nobody knows about."

@webapp.route("/secret/<name>/")
def secretName(name):
    return f"Congratulations, {name}, you have found the secret hidden webpage that nobody knows about."

if __name__=="__main__":
    webapp.run(port=4200, debug=True)
