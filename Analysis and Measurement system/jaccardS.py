import csv

def intersection(reddit,twitter) :
  
    intersect = reddit & twitter
    return intersect; 
  
  

def jaccard_index(reddit, twitter) :
      
    size_reddit = len(reddit); 
    size_twitter = len(twitter); 
    intersect = intersection(reddit, twitter); 
    size_in = len(intersect); 
    jaccard_in = size_in  / (size_reddit + size_twitter - size_in); 
  

    return jaccard_in; 
  
  

def jaccard_distance(jaccardIndex)  :
    jaccard_dist = 1 - jaccardIndex; 

    return jaccard_dist; 
 
def main():
    twitter = []
    with open("sentences.csv", "r") as fileT:
        csvreader = csv.reader(fileT)
        header = next(csvreader)
        for row in csvreader:
            twitter.append(row)
    
    reddit = []
    with open("sentencesReddit.csv", "r") as fileR:
        csvreader = csv.reader(fileR)
        header = next(csvreader)
        for row in csvreader:
            reddit.append(row)


    jaccardIndex = jaccard_index(reddit,twitter)
    print("Jaccard Index:"+jaccard_index)
    print("Jaccard Distance:"+jaccard_distance(jaccardIndex))


if __name__ == "__main__":
    main()