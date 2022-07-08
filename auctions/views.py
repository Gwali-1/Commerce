from email import message
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User,Listing,Comment,Category,Bids,Watchlist


def index(request):
    active_listings = Listing.objects.filter(active=True).order_by('created')
    print(active_listings)
    return render(request, "auctions/index.html",{
        "active_listings":active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first = request.POST["firstname"]
        last = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,first_name=first,last_name=last)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required()
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        description = request.POST["description"]
        price = float(request.POST["price"])
        image_link = request.POST["image_url"]

        print(request.POST)
        if not title or not price or not category or not description:
            return render(request, "auctions/createListing.html", {
                "message":"mMissing fields, please provide all information"
            })

        print(request.POST)

        #TODO  create listing, create category , add listing to user , add listing to category but first check if category exixt then add to existing if not create new 
        #category and add listing
        try:
            user = User.objects.get(pk=request.user.id)
            listing=Listing.objects.create(title=title.title(),description=description.capitalize(),price=price,ListingImageUrl=image_link,user=user)
            listing.save()
            # if check:
            #     check.listing
            category=Category(name=category.upper(),listing=listing)
            category.save()
            print("listing added")
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            print(e)
            return render(request,"auctions/createListing.html",{
                "message":"Couldnt create listing"
            })

    return render(request,"auctions/createListing.html")










def categories(request):
    return render(request,"auctions/categories.html")