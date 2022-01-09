import requests
from dotenv import load_dotenv
from os import environ
load_dotenv()


URL = "https://api.twitter.com/2"

class User:
    def __init__(self):
        self.headers = {
        'Authorization':'Bearer '+str(environ["BEARER_TOKEN"]),
        }
        # self.max_tweets=10
        # self.tweetfields='id,created_at'

    def jsondata(self,method,url):
        robj= requests.request(method, url, headers=self.headers)
        return robj.text
    
    def get_user(self,username=None,userid=None):
        if(userid):
            userid_url = URL +'/users/' + userid
            return self.jsondata('GET',userid_url)
        if(username):
            username_url = URL +'/users/by/username/' + username
            print(username_url)
            return self.jsondata('GET',username_url)        



class Tweet(User):
    def __init__(self,max_tweets=10,tweetfields='id,created_at'):
        super().__init__()
        self.tweetfields=tweetfields
        self.max_tweets=max_tweets
    
    def tweetsbyid(self,userids):
        url_id=f'{URL}/tweets/?ids={userids}&tweet.fields={self.tweetfields}'
        return self.jsondata('GET',url_id)

    def get_all_tweets(self,userid,pagination_token=None):
        userid_url = f'{URL}/users/{userid}/tweets?tweet.fields={self.tweetfields}&max_results={self.max_tweets}'
        if(not pagination_token):
            pass
        else:
            userid_url +=f'&pagination_token={pagination_token}'
        return self.jsondata('GET',userid_url)
    

