import requests
from dotenv import load_dotenv
from os import environ
import json
load_dotenv()


URL = 'https://api.twitter.com/2'

# user fields that we want to display in json
USER_DETAILS=['created_at', 'description', 'entities', 'id',
              'location', 'name', 'pinned_tweet_id', 'profile_image_url', 
              'protected', 'public_metrics', 'url', 'username',
              'verified','withheld']
# Tweet fields that we want to display in json
TWEET_DETAILS=['attachments', 'author_id', 'context_annotations', 
                'created_at', 'entities', 'geo', 
                'id', 'lang']


class User:
    def __init__(self):
        """ adding beartoken in the header """
        self.headers = {
        'Authorization':'Bearer '+str(environ["BEARER_TOKEN"]),
        }


    def jsondata(self,method,url):
        """ return python object from response """
        robj= requests.request(method, url, headers=self.headers)
        return json.loads(robj.text)
    
    def get_user(self,username=None,userid=None,USER_DETAILS=USER_DETAILS):
        """ function that return user details if userid or username is given """
        if(userid):
            userid_url = URL +'/users/' + userid + '?user.fields=' + ','.join(USER_DETAILS)
            return self.jsondata('GET',userid_url)

        if(username):
            username_url = URL +'/users/by/username/' + username + '?user.fields=' + ','.join(USER_DETAILS)
            print(username_url)
            return self.jsondata('GET',username_url)
  


class Tweet(User):
    def __init__(self,max_tweets=10,tweetfields='id,created_at'):
        """ setting limits to tweets if required"""
        super().__init__()
        self.tweetfields=tweetfields
        self.max_tweets=max_tweets
    
    def tweetsbyid(self,userids):
        """ getting the user's tweet if the id is passed """
        url_id=f'{URL}/tweets/?ids={userids}&tweet.fields={self.tweetfields}'
        return self.jsondata('GET',url_id)

    def get_all_n_day(self,userid,days):
        """ get tweets from n days """
        tweet_url = f'{URL}/users/{userid}/tweets?start_time={days}&max_results=99&tweet.fields='+','.join(TWEET_DETAILS)
        return self.jsondata('GET',tweet_url)

    

