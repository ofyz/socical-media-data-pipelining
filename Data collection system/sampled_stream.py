import requests
import os
import json
import pymongo
from pymongo import MongoClient
from bson import json_util
import time


bearer_token = "";
cluster = MongoClient("mongodb+srv:....")
db= cluster["socialMedia"]
collection1 = db["retrievec"]
collection2 = db["test"]

dataDict = {}


def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=lang,context_annotations,public_metrics,possibly_sensitive,source&expansions=author_id&user.fields=public_metrics,verified"


def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url):
    tweetCount =0
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if json_response["data"]["lang"]=="en":
                
                collection1.insert_one(parse_json(json_response))
                tweetCount+=1
                #print(tweetCount)
                print(json.dumps(json_response, indent=4, sort_keys=True))
                
                    
                
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
           
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

def parse_json(data):
    return json.loads(json_util.dumps(data))


    
def main():
    url = create_url()
    timeout = 0
    while True:

        connect_to_endpoint(url)
        timeout += 1


    

if __name__ == "__main__":
    main()