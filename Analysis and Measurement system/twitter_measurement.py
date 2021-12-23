from bson.objectid import ObjectId
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from pymongo import MongoClient, cursor
import re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import csv



bearer_token = "";
cluster = MongoClient("")
db= cluster["socialMedia"]
collection1 = db["retrievec"]
collection2 = db["reddit"]

""" df = pd.DataFrame(list())
df.to_csv("sentences.csv") """

#what is the positive/negative expression ratio of the collected tweets and reddit titles
def twitter_calculation():
    
    analyser = SentimentIntensityAnalyzer() 

    cursor = collection1.find({})
    for obj in cursor:
        sentence = obj["data"]["text"]
        mongoObjectid= obj["_id"]
            
        #calculating scores
        result = analyser.polarity_scores(sentence)
        if result["compound"] >= 0.05:
            collection1.update({ "_id": ObjectId(mongoObjectid)},{"$set" : {"result":"Positive"}})
            print("Result:"+"Positive")
        elif result["compound"] <= -0.05:
            collection1.update({ "_id": ObjectId(mongoObjectid)},{"$set" :  {"result":"Negative"}})
            print("Result:"+"Negative")
        else:
            collection1.update({ "_id": ObjectId(mongoObjectid)},{"$set" :  {"result":"Neutral"}})
            print("Result:"+"Neutral")

        #saving scores to database
        collection1.update({ "_id": ObjectId(mongoObjectid)},{"$set" : result})

        print("Text:"+sentence)


#bunu yapmak icin her iki platformun word clooudunu olusturabilirim ??

def create_csv_file():
    
    with open('sentences.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        cursor = collection1.find({})
        for obj in cursor:
            sentence = obj["data"]["text"]

            mongoObjectid= obj["_id"]
            print(sentence)
            newSentence = clean_text(sentence)
            print(newSentence)
            print("----------")
            writer.writerow([newSentence])
            print(newSentence)

def word_cloud():
    df = pd.read_csv(r'sentences.csv',encoding="latin-1")
    comment_words = ""
    stopwords = set(STOPWORDS)

    for val in df.CONTENT:
        val= str(val)
        tokens = val.split()
        print("inside excell")

            
        for i in range(len(tokens)):
            print("Iside tokens")
            tokens[i] = tokens[i].lower()
     
            comment_words += " ".join(tokens)+" "
 
            wordcloudHere = WordCloud(width = 800, height = 800,
                background_color ='white',
                max_words=200,
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


def calculate_positive_negative():
    positiveCounter = 0
    counter = 0
    negativeCounter = 0
    notrCounter = 0
    cursor = collection1.find({})
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
    
    #twitter_calculation()
    #calculate_positive_negative()
    #clean_text()
    word_cloud()
    #create_csv_file()
if __name__ == "__main__":
    main()
    