from django.shortcuts import render
from .models import Tweet
from .forms import tweetForm, userRegistrationForm, tweetSearch
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


# Create your views here.
def index(request):
    return render(request, "index.html")


# List all the tweets
def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    if request.method == 'GET':
        form = tweetSearch(request.GET)
        if form.is_valid():
            userName = form.cleaned_data['searchData']
            tweets = Tweet.objects.filter(user__username=userName)
            return render(request, "tweet_search.html", {"tweets": tweets, "form":form})
        else:
            form = tweetSearch()
        return render(request, "tweet_search.html", {"form": form, "tweets": tweets});
        

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = tweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweetData = form.save(commit=False)
            tweetData.user = request.user
            tweetData.save()
            return redirect("tweet_list")
    else:
        form = tweetForm()
    return render(request, "tweet_form.html", {"form": form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = tweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweetData = form.save(commit=False)
            tweetData.user = request.user
            tweetData.save()
            return redirect("tweet_list")
    else:
        form = tweetForm(instance=tweet)
    return render(request, "tweet_form.html", {"form": form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request, "tweet_confirm_delete.html", {"tweet": tweet})


# @login_required
def user_register(request):
    if request.method == "POST":
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = userRegistrationForm()
    return render(request, "registration/registration.html", {"form": form})

def user_logout(request):
    if request.method=='POST':
        logout(request) 
        request.session.flush()
        return redirect('Home')
    return render(request, "registration/logout.html")
