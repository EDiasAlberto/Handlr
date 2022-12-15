import pymongo, os, random
from dotenv import load_dotenv

#Class containing functions managing users and accounts
class VerifyFuncs: 
    #Initialises class and creates connection to database accounts collection
    def __init__(self, databaseURL):
        __client = pymongo.MongoClient(databaseURL)
        __db = __client.handlr_database
        #Defines the connection as a private variable to prevent unauthorised changes
        self.__collection = __db["accounts"]

    #Verifies the inputted user details to authenticate users
    def verifyUsr(self, username, password):
        #Checks if a user with the same username-password combo exists in the database
        result = self.__collection.find_one({"username": username.lower(), "password":password})
        #If not, the user is not authenticated
        if result is None:
            return False
        #If so, the user is authenticated
        return True

    def updatePass(self, username, oldPassword, newPassword, confirmPassword):
        result = self.__collection.find_one({"username": username.lower(), "password":oldPassword})
        print(username, oldPassword)
        print(newPassword, confirmPassword)
        print(result)
        isValid=True
        if (result is None) or (newPassword!=confirmPassword):
            isValid=False
            return isValid
        self.__collection.update_one({"username":username.lower()}, {"$set":{"password":newPassword}})
        return isValid

    def newUsr(self, username, password, confirmPassword):
        if password!=confirmPassword:
            return "The passwords do not match."
        elif self.__collection.find_one({"username":username.lower()})!=None:
            return "That account already exists."
        self.__collection.insert_one({"username":username.lower(), "password":password})

