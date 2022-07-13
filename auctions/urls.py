from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/",views.create,name="create"),
    path("categories/",views.categories,name="categories"),
    path("listing/<int:id>",views.listing_info,name="ListingInfo"),
    path("newbid/<int:id>",views.new_bid,name="NewBid"),
    path("addcomment/<int:id>",views.add_comment,name="comment"),
    path("close/<int:id>",views.close_auction,name="close_auction"),
    path("addtowatchlist/<int:id>",views.add_to_watchlist,name="add_to_watchlist"),
    path("watchlist/",views.watchlist,name="watchlist"),
]
