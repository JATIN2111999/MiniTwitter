from modules.helper import User,Tweet
import json
from pprint import pprint
server =Tweet()

userdata=server.get_user(username='jatinhabibkar')

data=server.tweetsbyid(userids='20')
print(data)



usertweet = server.get_all_tweets('478432912')
pprint(usertweet)