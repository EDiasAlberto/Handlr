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

    def postQuestion(self, postTitle, postAuthor, question, questionOwner):
        question = {
            "listingTitle" : postTitle,
            "listingOwner" : postAuthor,
            "questionText" : question,
            "questionOwner": questionOwner,
            "Responses" : []
        }
        self.collection.insert_one(question)
        return True

    def ansQuestion(self, postTitle, postAuthor, question, questionOwner, answer):
        filter = {
            "listingTitle" : postTitle,
            "listingOwner" : postAuthor,
            "questionText" : question,
            "questionOwner": questionOwner
        }
        question = self.collection.find_one(filter)
        print(question)
        responses=[]
        if question is not None:
            responses = list(question["Responses"])
        responses.append(answer)
        update = {
            "$set" : {
                "Responses" : responses
            }
        }
        self.collection.update_one(filter, update)

        
