from pymongo import MongoClient
from dotenv import load_dotenv
from os import environ
load_dotenv()
client = MongoClient(environ["MONGOURI"])
db=client.get_database("tweets")

def insert_all_data(data,title):
    """ insert all tweet in database with title as collection name """
    mycol = db[title]
    if(not data.get('data') or len(data['data'])==0):
        return "sorry we cannot save that tweets it may me empty or error responze"
    try:
        mycol.insert_many(data['data'])
        return True
    except Exception as e:
        print(e,'something went wrong')

def get_all_coll(search,coll):
    """ get all the records from specific collection """
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
    """ get all record from all collection present in mongodb server """
    l=[]
    for coll in db.list_collection_names():
        mycol = db.get_collection(coll)
        for x in mycol.find({},{'_id':0}):
            if str(search.lower()) in x["text"].lower():
                print(x['text'])
                l.append(x)
    return l

def get_collections():
    """ get the name and count of collection and document present on the mongodb server"""
    l=[]
    # col=(db.get_collection('todaystweet'))
    # print(col.count_documents({}))
    for c in db.list_collection_names():
        nl={
            "name":c,
            "count":db.get_collection(c).count_documents({})
        }
        l.append(nl)
    return l