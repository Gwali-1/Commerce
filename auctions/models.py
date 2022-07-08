from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass




class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    price =models.FloatField()
    active = models.BooleanField(default=True)
    bid_number = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="listings")
    ListingImageUrl = models.CharField(max_length=200,blank=True)
    created = models.DateField(default= datetime.now().strftime('%Y-%m-%d'))

    def __str__(self):
        return f'{self.title} {self.price} {self.active} {self.bid_number}'
   

class Comment(models.Model):
    comments = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comments")

    def __str__(self):
        return f"{self.comments}"


class Category(models.Model):
    name = models.CharField(max_length=64)
    listing= models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="categories")

    def __str__(self):
        return f"{self.name} {self.listing}"



class Bids(models.Model):
    bid = models.IntegerField()
    state = models.CharField(default="unresolved",max_length=64)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bid_info")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="Bids")

    def __str__(self):
        return f"{self.bid} {self.listing}"

class Watchlist(models.Model):
    Listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="listings")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="wachlist")

    def __str__(self):
        return f"{self.user} {self.Listing}"
        