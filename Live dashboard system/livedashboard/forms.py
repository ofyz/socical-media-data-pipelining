from django import forms

class CreateSubredditName(forms.Form):
    subreddit_text = forms.CharField(max_length=40)