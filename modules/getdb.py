from pymongo import MongoClient
from dotenv import load_dotenv
from os import environ
load_dotenv()
client = MongoClient(environ["MONGOURI"])
db=client.get_database("tweets")

def insert_all_data(data,title):
    mycol = db[title]
    try:
        mycol.insert_many(data['data'])
    except Exception as e:
        print(e,'something went wrong')

def get_all_coll(search,coll):
    try:
        mycol = db.get_collection(coll)
        l=[]
        print(search)
        for x in mycol.find({},{'_id':0}):
            if str(search.lower()) in x["text"].lower():
                print(x['text'])
                l.append(x)
        return l
    except Exception as e:

        print(e,'something went wrong')
def get_all(search):
    l=[]
    for coll in db.list_collection_names():
        mycol = db.get_collection(coll)
        for x in mycol.find({},{'_id':0}):
            if str(search.lower()) in x["text"].lower():
                print(x['text'])
                l.append(x)
    return l
