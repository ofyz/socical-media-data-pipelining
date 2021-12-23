import json
import requests
import pandas as pd
import base36
import pymongo
from pymongo import MongoClient
from bson import json_util

bearer_token = "";
cluster = MongoClient("mongodb+srv:....")
db= cluster["socialMedia"]
collection1 = db["retrieved"]
collection2 = db["reddit"]

client_id=""
secret_key =""
username =''
password =""
user_agent=""

auth = requests.auth.HTTPBasicAuth(client_id,secret_key)
data ={'grant_type':'password',
        'username':username,
        'password':password}

headers = {'User-Agent':'MyAPI/0.0.1'}

res =requests.post('https://www.reddit.com/api/v1/access_token',auth=auth,data=data,headers=headers)

token = res.json()['access_token']
headers['Authorization'] = f'bearer {token}'


pd.set_option('display.expand_frame_repr', False)

df = pd.DataFrame()
dataDict={}

def parse_json(data):
    return json.loads(json_util.dumps(data))

def main():
    #requesting posts batches of hundred and some posts are repeated not big deal and some posts are missing MAX 100 POST
    while True:    
        df = pd.DataFrame()
        id=0;
        counter=0;
        timeout = 0;
        output = requests.get('https://oauth.reddit.com/r/all/new?limit=1',headers=headers)
        
        for post in output.json()["data"]["children"]:
            postID = post["data"]["id"]
            id = base36.loads(postID)
            print(id)
        
        for i in range(10):
            output = requests.get('https://oauth.reddit.com/r/all/new?limit=100&after=t3_',base36.dumps(id),headers=headers)
            id=id-100

            for post in output.json()["data"]["children"]:
                df= df.append({"ID":base36.loads(post["data"]["id"]),"Subreddit":post["data"]["subreddit"],"title":post["data"]["title"],"NumId":base36.loads(post["data"]["id"])},ignore_index= True)
                
                dataDict ={"subreddit": post["data"]["subreddit"],"title":post["data"]["title"],"selftext":post["data"]["selftext"],"permalink":post["data"]["permalink"],"url":post["data"]["url"]}
                collection2.insert_one(dataDict)
                
                print("ID:"+str(base36.loads(post["data"]["id"])) +"  "+"Subreddit"+" "+str(counter)+":"+post["data"]["subreddit"])
                counter+=1

        
if __name__ == "__main__":
    main()
       
        