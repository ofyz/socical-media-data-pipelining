# Generated by Django 3.2.9 on 2021-12-13 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reddit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subreddit', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=500)),
                ('sentiment_result', models.CharField(max_length=500)),
                ('text_link_ratio_flag', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compound', models.CharField(max_length=500)),
                ('neg', models.CharField(max_length=500)),
                ('neu', models.CharField(max_length=500)),
                ('pos', models.CharField(max_length=500)),
                ('result', models.CharField(max_length=500)),
                ('retweet_count', models.IntegerField()),
                ('like_count', models.IntegerField()),
                ('quote_count', models.IntegerField()),
                ('follower_count', models.IntegerField()),
                ('following_count', models.IntegerField()),
                ('tweet_count', models.IntegerField()),
                ('listed_count', models.IntegerField()),
                ('verified', models.BooleanField()),
                ('sentiment_result', models.CharField(max_length=500)),
                ('source', models.CharField(max_length=500)),
                ('possibly_sensetive', models.BooleanField()),
            ],
        ),
    ]
