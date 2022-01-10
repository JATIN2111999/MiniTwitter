import collections
from flask import Flask,make_response
from flask import jsonify
from flask import Flask,render_template,redirect, url_for,request
from flask_restful import reqparse, abort, Api, Resource
from modules.getdb import get_all_coll, get_collections, insert_all_data, get_all,client
from modules.helper import User,Tweet
from datetime import datetime,timedelta
from pymongo import MongoClient
from pymongo.errors import OperationFailure

t= Tweet()

app = Flask(__name__)

api =Api(app)


class Index(Resource):
    def get(self):
        try:
            client.get_database()
            return{'message':'Data Base Connection Established........'},200

        except OperationFailure as err:
            return (f"Data Base Connection failed. Error: {err}"),503


def checkerrors(data):
    if(data.get('errors') or data.get('error')):
        return True
    else:
        return False

class Username(Resource):
    def get(self, username):
        try:
            data=t.get_user(username=username)
            if(checkerrors(data)):
                return data, 400
            return data,200
        except Exception as e:
            return 'something went wrong on server side',500


class Userid(Resource):
    def get(self,userid):
        try:
            data=t.get_user(userid=userid)
            if(checkerrors(data)):
                return data, 400
            return data, 200
        except Exception as e:
            return 'something went wrong on server side',500


class Last_n_days(Resource):
    def get(self,userid,days):
        try:
            today_date= datetime.now() +timedelta(days=0-days)
            past_day=today_date.strftime("%Y-%m-%dT00:00:00.%f")[:-4]+"Z"
            data = t.get_all_n_day(userid,past_day)
            if(checkerrors(data)):
                return data, 400
            return data,200
        except Exception as e:
            return 'something went wrong on server side',500

    def post(self,userid,days):
        if(request.json):
            if not request.json.get('title'):
                return {"message":"plz specify a title ","got":{
                    "title":request.json.get('title')
                }}, 400
            today_date= datetime.now() +timedelta(days=0-days)
            past_day=today_date.strftime("%Y-%m-%dT00:00:00.%f")[:-4]+"Z"
            data = t.get_all_n_day(userid,past_day)

            if(checkerrors(data)):
                return data, 400
            message=insert_all_data(data,title=request.json.get('title'))
            if(message==True):
                return {"message":"saved in data with title "+ request.json.get('title') },200
            else:
                return {"message":message},400

        else:
            return {"message":"plz specify a title ","got":{
                    "title":"null"
                }}, 400


class Database(Resource):
    def get(self):
        key_word= request.args.get('search')
        key_coll= request.args.get('coll')
        filtered_data=[]
        if(key_coll and key_word):
            filtered_data=get_all_coll(key_word,key_coll)
        if(key_word):
            filtered_data=get_all(key_word)
        return {"data":filtered_data,'count':len(filtered_data)
        ,'search':request.args.get('search')
        ,'coll':request.args.get('coll')},200   


class Coll(Resource):
    def get(self):
        all_col =get_collections()
        return {'collections':all_col,'count':len(all_col)},200

api.add_resource(Username, '/v1/username/<string:username>')
api.add_resource(Userid, '/v1/userid/<string:userid>')
api.add_resource(Last_n_days,'/v1/userid/<string:userid>/<int:days>')
api.add_resource(Database,'/v1/db')
api.add_resource(Coll,'/v1/collections')
api.add_resource(Index,'/')


if __name__ == '__main__':
    app.run(debug=True)
