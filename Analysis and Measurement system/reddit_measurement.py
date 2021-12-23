from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from pymongo import MongoClient, cursor
from bson.objectid import ObjectId
import re
import csv
import matplotlib.pyplot as plt
from wordcloud import wordcloud
from wordcloud.wordcloud import STOPWORDS, WordCloud
import emoji
import regex


bearer_token = "";
cluster = MongoClient("")
db= cluster["socialMedia"]
collection1 = db["retrievec"]
collection2 = db["reddit"]


""" df = pd.DataFrame(list())
df.to_csv("sentencesReddit.csv")  """


#what is the positive/negative expression ratio of the collected tweets and reddit titles
def reddit_calculation():
    positiveCounter = 0
    counter = 0
    negativeCounter = 0
    notrCounter = 0
    
    analyser = SentimentIntensityAnalyzer() 

    cursor = collection2.find({})
    for obj in cursor:
        sentence = obj["title"]
        mongoObjectid= obj["_id"]
            
        #calculating scores
        result = analyser.polarity_scores(sentence)
        if result["compound"] >= 0.05:
            collection2.update({ "_id": ObjectId(mongoObjectid)},{"$set" : {"result":"Positive"}})
            positiveCounter+=1
            counter+=1
            print("Positive counter:"+str(positiveCounter))
            print("Counter:"+str(counter))
        elif result["compound"] <= -0.05:
            collection2.update({ "_id": ObjectId(mongoObjectid)},{"$set" :  {"result":"Negative"}})
            negativeCounter+=1
            counter+=1
            print("Negative counter:"+str(negativeCounter))
            print("Counter:"+str(counter))
            #print("Result:"+"Negative")
        else:
            collection2.update({ "_id": ObjectId(mongoObjectid)},{"$set" :  {"result":"Neutral"}})
            notrCounter+=1
            counter+=1
            print("notr counter:"+str(notrCounter))
            print("Counter:"+str(counter))
            #print("Result:"+"Neutral")

        #saving scores to database
        collection2.update({ "_id": ObjectId(mongoObjectid)},{"$set" : result})

        #print("Text:"+sentence)

#what is the text/link ratio of reddit post's selftext field
def text_link_ratio():
    linkCounter = 0
    textCounter = 0
    totalCounter = 0
    cursor = collection2.find({})
    for obj in cursor:
        sentence = obj["selftext"]
        mongoObjectid= obj["_id"]

        text_ratio_flag= re.search("^https://",sentence)

        if text_ratio_flag:
            #print("There is a link inside the self text field")
            collection2.update({ "_id": ObjectId(mongoObjectid)},{"$set" :  {"text_link_ratio_flag":"1"}})
            linkCounter+=1
            totalCounter+=1
            print("Link:"+str(linkCounter))
            print("Total:"+str(totalCounter))
        else:
            #print("There is not link inside the self text field")
            collection2.update({ "_id": ObjectId(mongoObjectid)},{"$set" :  {"text_link_ratio_flag":"0"}})
            textCounter+=1
            totalCounter+=1
            print("Text:"+str(textCounter))
            print("Total:"+str(totalCounter))
            #print(sentence)
            print("Text-Link Ratio:"+obj["text_link_ratio_flag"])


#bunu yapmak icin her iki platformun word clooudunu olusturabilirim ??

def create_csv_file():

    with open('sentencesReddit.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        cursor = collection2.find({})
        for obj in cursor:
            sentence = obj["title"]
            mongoObjectid= obj["_id"]
            print(sentence)
            newSentence = clean_text(sentence)
            print(newSentence)
            print("----------")
            writer.writerow([newSentence])
            print(newSentence)

def word_cloud():
    df = pd.read_csv(r'sentencesReddit.csv',encoding="latin-1")
    comment_words = ""
    stopwords = set(STOPWORDS)

    for val in df.CONTENT:
        val= str(val)
        tokens = val.split()
        print("inside excell")

            # Converts each token into lowercase
        for i in range(len(tokens)):
            print("Iside tokens")
            tokens[i] = tokens[i].lower()
     
            comment_words += " ".join(tokens)+" "
 
            wordcloudHere = WordCloud(width = 800, height = 800,
                background_color ='white',
                max_words=20,
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloudHere)
    plt.axis("off")
    plt.tight_layout(pad = 0)
 
    plt.show()

def clean_text(sentence):
 
    print ("initial string : ", sentence)
  
    result = re.sub(r'\W+', ' ', sentence)
    #result = re.sub("[ãØÙ©§]", " ",sentence)
    return result

def calculate_ratio():
    positiveCounter = 0
    counter = 0
    negativeCounter = 0
    notrCounter = 0
    cursor = collection2.find({})
    for obj in cursor:
        sentence = obj["result"]
        if sentence == "Positive":
            positiveCounter+=1
            counter+=1
            print("Counter:"+str(counter))
            print("Positive counter:"+str(positiveCounter))
        elif sentence == "Negative":    
            negativeCounter+=1
            counter+=1
            print("Counter:"+str(counter))
            print("Positive counter:"+str(negativeCounter))
        else:
            counter+=1
            notrCounter+=1
            print("Counter:"+str(counter))
            print("Neutral counter:"+str(notrCounter))


def main():
    #create_csv_file()
    #reddit_calculation()
    text_link_ratio()
    #word_cloud()
    #calculate_ratio()
if __name__ == "__main__":
    main()
    