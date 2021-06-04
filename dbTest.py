import pymongo
client = pymongo.MongoClient("mongodb+srv://handlrFile:4iF64ZEgFbdgTFDE@handlr.5hllv.mongodb.net/test_database?retryWrites=true&w=majority")
db = client.test_database
collection = db["test_collection"]
result = collection.find_one({"username": "ethan"})
if result is None:
    print("user does not exist")
else:
    print(result)