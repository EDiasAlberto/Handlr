import pymongo, os, random
from dotenv import load_dotenv



def verifyUsr(username, password):
    databaseURL = os.getenv("databaseURL")
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["accounts"]
    result = collection.find_one({"username": username.lower(), "password":password})
    if result is None:
        return False
    return True

def newUsr(username, password, confirmPassword):
    databaseURL = os.getenv("databaseURL")
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["accounts"]
    if password!=confirmPassword:
        return "The passwords do not match."
    elif collection.find_one({"username":username.lower()})!=None:
        return "That account already exists."
    collection.insert_one({"username":username.lower(), "password":password})

