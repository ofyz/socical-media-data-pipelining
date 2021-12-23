from django.forms import forms
from django.shortcuts import render
from django.http import HttpResponse, response
from pymongo import MongoClient, cursor, database
from django import forms


import mongoengine as db

cluster = MongoClient("mongodb+srv://<username>:<password>@cluster0.sehys.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db= cluster["socialMedia"]
collection1 = db["retrievec"]
collection2 = db["reddit"]
collection3 = db["scores"]


# Create your views here.


class CreateSubredditName(forms.Form):
    subreddit_text = forms.CharField()

class CreateTwitterSens(forms.Form):
    reddit_flag = forms.CharField()

def home(response):
    positiveCounterTW = 0
    negativeCounterTW = 0
    neutralCounterTW = 0 
    counterTW = 0
    number = []
    number2 = []
    number3 = []
    cursor = collection3.find({})
    for obj in cursor:
        if obj["reddit_total"] == 0:
            print("Something is wrong")
        else:
            number.append(obj["reddit_total"])
            number.append(obj["reddit_positive"])
            number.append(obj["reddit_negative"])
            number.append(obj["reddit_neutral"])
        
            print("Done1")

        if obj["twitter_total"] == 0:

            print("Something is wrong")
        else:
            number2.append(obj["twitter_total"])
            number2.append(obj["twitter_positive"])
            number2.append(obj["twitter_negative"])
            number2.append(obj["twitter_neutral"])

            print("Done2")
    
    subreddit_text = ""
    if response.method == 'GET':
        form = CreateSubredditName(response.GET)
        print("Done4")
        
    if form.is_valid():
        positiveCounter = 0
        negativeCounter = 0
        neutralCounter = 0 
        counter2 = 0
        print("Done5")
        subreddit_text = form.cleaned_data['subreddit_text']

        if subreddit_text != " ":

            cursor = collection2.find({})
            
            for obj in cursor:
                if counter2 < 120000:
                    if obj["subreddit"] != "xpxpxpxpxp" :
                        counter2 = counter2+1
                        print("Subreddit Counter:"+str(counter2))
                        print("Result:"+str(counter2) +"-"+obj["result"])
                        if obj["subreddit"] == subreddit_text and obj["result"] == "Positive":
                            positiveCounter = positiveCounter+1
                            print("Positive:" +str(positiveCounter))
                        elif obj["subreddit"] == subreddit_text and obj["result"] == "Negative":
                            negativeCounter = negativeCounter+1
                            print("Negative:" +str(negativeCounter))
                        elif obj["subreddit"] == subreddit_text and obj["result"] == "Neutral":
                            neutralCounter = neutralCounter+1
                            print("Neutral:" +str(neutralCounter))

                        
                else:
                    break
            
            return render(response,"livedashboard/home.html",{"number_list":number,"number_list2":number2,"subreddit":subreddit_text,
        "positive":positiveCounter,"negative":negativeCounter,"neutral":neutralCounter,
        "pos":positiveCounterTW,"neg":negativeCounterTW, "neut":neutralCounterTW})
                    
    #-------------------
    reddit_flag = ""
    if response.method == 'GET':
        form = CreateTwitterSens(response.GET)
        print("Done4")

    if form.is_valid():
        positiveCounterTW = 0
        negativeCounterTW = 0
        neutralCounterTW = 0 
        counterTW = 0

        reddit_flag = form.cleaned_data['reddit_flag']

        cursor = collection1.find({})
        
        for obj in cursor:
            if counterTW < 5000:
                if obj["data"]["possibly_sensitive"] == True :
                    counterTW = counterTW+1
                    print("Tweet Counter:"+str(counterTW))
                    print("Result:"+str(counterTW) +"-"+obj["result"])
                    if obj["result"] == "Positive":
                        positiveCounterTW = positiveCounterTW+1
                        print("Positive TW:" +str(positiveCounterTW))
                    elif obj["result"] == "Negative":
                        negativeCounterTW = negativeCounterTW+1
                        print("Negative TW:" +str(negativeCounterTW))
                    elif obj["result"] == "Neutral":
                        neutralCounterTW = neutralCounterTW+1
                        print("Neutral TW:" +str(neutralCounterTW))
            else:
                break


        return render(response,"livedashboard/home.html",{"number_list":number,"number_list2":number2,"subreddit":subreddit_text,
       """  "positive":positiveCounter,"negative":negativeCounter,"neutral":neutralCounter, """
        "pos":positiveCounterTW,"neg":negativeCounterTW, "neut":neutralCounterTW})

    return render(response,"livedashboard/home.html",{"number_list":number,"number_list2":number2})

