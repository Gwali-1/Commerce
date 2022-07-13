from email import message
from tabnanny import check
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User,Listing,Comment,Category,Bids,Watchlist


#index page
def index(request):
    active_listings = Listing.objects.filter(active=True).order_by('-created')

    #if user is logged in , add watchlist object
    if request.user.is_authenticated:
         watchlist = Watchlist.objects.filter(user=request.user)
         return render(request, "auctions/index.html",{
        "active_listings":active_listings,
        "watchlist":watchlist,
    })

    print(active_listings)
    return render(request, "auctions/index.html",{
        "active_listings":active_listings,
    })





#login
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


#logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))




#register
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



#create listing
@login_required()
def create(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    categories_available =  Category.objects.all()
    print(categories_available)
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        description = request.POST["description"]
        price = request.POST["price"]
        image_link = request.POST["image_url"]

        print(request.POST)
        if not title or not price or not category or not description:
            messages.error(request,"Error: Missing Fields")
            return render(request, "auctions/createListing.html")


        #TODO  create listing, create category , add listing to user , add listing to category but first check if category exixt then add to existing if not create new 
        #category and add listing
        try:
            user = User.objects.get(pk=request.user.id)
            listing=Listing.objects.create(title=title.title(),description=description.capitalize(),price=float(price),ListingImageUrl=image_link,user=user)
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

    return render(request,"auctions/createListing.html",{
        "watchlist":watchlist,
        "available_categories":categories_available,
    })




def listing_info(request,id):
    ''' gets a listing objects and other information associated to it'''
    listing = Listing.objects.get(pk=id)
    category_name  = Category.objects.get(listing=listing)
    comments = Comment.objects.filter(listing=listing).order_by("comments")

    if request.user.is_authenticated:
         watchlist = Watchlist.objects.filter(user=request.user)

    #if not logged in
    if not request.user.is_authenticated:
        return render(request,"auctions/listing.html",{
        "listing":listing,
        "category":category_name,
        "comments":comments,
    })


    if listing.bid_number > 0:
        winning_bid = Bids.objects.get(bid=listing.price)
        return render(request,"auctions/listing.html",{
        "listing":listing,
        "category":category_name,
        "comments":comments,
        "bid":winning_bid,
        "watchlist":watchlist
    })
    
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "category":category_name,
        "comments":comments,
        "watchlist":watchlist
    })



#Bid
@login_required()
def new_bid(request,id):
    ''' places a bid on the listing and makes it the current price if its larger than all other bids
        also updates the bid number on listing
    '''
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        if not (new_bid := request.POST["bid"]):
            messages.error(request,"Please enter a bid amount")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))

        if not new_bid.isnumeric():
            messages.error(request,"Please enter a valid amount")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))

        if listing.active == False:
            messages.error(request,"Cannot Bid on Closed auction")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))

        if float(new_bid) > listing.price:
            try:
                user = User.objects.get(pk=request.user.id)
                new_bid_on_listing = Bids.objects.create(bid=new_bid,user=user,listing=listing)
                new_bid_on_listing.save()
                print("bid added")
                listing.bid_number += 1
                listing.price = new_bid
                listing.save()
                print("listing updated")
                messages.success(request,"SUCCESS: Your Bid Has Been Added")
                return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))
            except Exception as e:
                print(e)
                messages.info(request,"INFO: Could Not Add Your Bid At The Moment, Try Again Later")
                return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))

        messages.error(request,"Error:Bid Must Be Greater Than Current Price To Be Added")
        return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))






#comment
@login_required()
def add_comment(request,id):
    ''' adds a comment to the listing page'''

    if request.method == "POST":
        listing = Listing.objects.get(pk=id)

        #if not comment was sent
        if not (comment := request.POST["comment"]):
            messages.error(request,"no comment provided")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))

        #try to save comment    
        try:
            new_comment = Comment.objects.create(comments=comment.strip(),listing=listing)
            new_comment.save()
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))
        except Exception as e:
            print(e)
            messages.info(request,"INFO: Could Not Add Your Comment At The Moment, Try Again Later")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))



# watchlist
@login_required()
def add_to_watchlist(request,id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        if (check := Watchlist.objects.filter(Listing=listing,user=request.user)):
            messages.info(request,"Item Is Already In Your Watchlist")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))
        try:
            new_watchlist = Watchlist.objects.create(Listing=listing,user=request.user)
            new_watchlist.save()
            print("added_watchlist")
            messages.success(request,"Added To Watchlist")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))
        except Exception as e:
            messages.info(request,"Could Not Add To Watchlist, Try again Later")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))



#close aunction
@login_required()
def close_auction(request,id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        if listing.user != request.user:
            messages.warning(request,"Creditial Forgery Detected")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))

    
        try:
            #if there are no bids on item
            if not (winning_bid := Bids.objects.filter(bid=listing.price,user=request.user,listing=listing)):
                listing.active = False
                listing.save()
                messages.success(request,"Auction Closed")
                return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))

            listing.active = False
            listing.save()
            winning_bid[0].state = "won"
            winning_bid[0].save()
            messages.success(request,"Auction Closed")
            return HttpResponseRedirect(reverse("ListingInfo",args=(listing.id,)))
        except Exception as e:
            messages.info(request,"Could Not Add To Watchlist, Try again Later")
            return HttpResponse("not ok")
        



#watchlist
@login_required()
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)

    if request.method == "POST":
        listing_id = request.POST["listing"]
        listing = Listing.objects.get(pk=listing_id)

        #if for some reason listing sent is not in users watchlist
        if not (chek := Watchlist.objects.filter(user=request.user,Listing=listing)):
            messages.warning(request,"Creditial Forgery Detected")
            return render(request,"auctions/watchlist.html",{
            "watchlist":watchlist
        
    })
        
        try:
            #remove
            Watchlist.objects.filter(user=request.user,Listing=listing).delete()
            messages.success(request,"Item removed from watchlist")
            return render(request,"auctions/watchlist.html",{
            "watchlist":watchlist
            })
        except Exception as e:
            print(e)
            messages.info(request,"Item could not be removed")
            return render(request,"auctions/watchlist.html",{
            "watchlist":watchlist
            })
            
 
    return render(request,"auctions/watchlist.html",{
        "watchlist":watchlist
        
    })




def categories(request):
    return render(request,"auctions/categories.html")