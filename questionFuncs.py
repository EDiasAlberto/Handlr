import pymongo, os

class QuestionFuncs:

    def __init__(self, databaseURL):
        self.client = pymongo.MongoClient(databaseURL)
        self.db = self.client.handlr_database
        self.collection = self.db["questions"]

    def fetchQuestions(self, postTitle, postAuthor):
        questions = self.collection.find({"listingTitle":postTitle, "listingOwner":postAuthor.lower()})
        questionList = [x for x in questions]
        return questionList
