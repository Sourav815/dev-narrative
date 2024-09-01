from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class tweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ["text", "photo"]


class tweetSearch(forms.Form):
    searchData = forms.CharField(label="Search By Username", max_length=100)



class userRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

