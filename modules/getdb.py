from pymongo import MongoClient
from dotenv import load_dotenv
from os import environ
load_dotenv()
print(environ["MONGOURI"])
client = MongoClient(environ["MONGOURI"])
db=client.get_database("tweets")
collection =db.get_collection("items")

# document=collection.find_one()

# cursor=collection.find()

# for each_documnet in cursor:

#     print(each_documnet["timstamp"])
