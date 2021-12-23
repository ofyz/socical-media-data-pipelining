from django.db import models

# Create your models here.
class Reddit(models.Model):
    subreddit = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    sentiment_result = models.CharField(max_length=500)
    text_link_ratio_flag = models.CharField(max_length=500) 



    
