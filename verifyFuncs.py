import pymongo, os, random
from dotenv import load_dotenv

class VerifyFuncs: 
    def __init__(self, databaseURL):
        client = pymongo.MongoClient(databaseURL)
        db = client.handlr_database
        self.collection = db["accounts"]


    def verifyUsr(self, username, password):
        result = self.collection.find_one({"username": username.lower(), "password":password})
        if result is None:
            return False
        return True

    def newUsr(username, password, confirmPassword):
        if password!=confirmPassword:
            return "The passwords do not match."
        elif self.collection.find_one({"username":username.lower()})!=None:
            return "That account already exists."
        self.collection.insert_one({"username":username.lower(), "password":password})

