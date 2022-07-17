
# ODD AUCTIONS(Commerce site)

*odd auctions is a web application implemented using the django web framework. The site works by giving users who have registered for an account the ability to make listings of products and also bid on products listed by other users. Users who create auctions have the abilty to close them and if the item had any  bids the winner is determined based on who was leading the bid at the moment of closing. This application is built purely with django and follows a typical layered achitecture pattern. The app has several view fuctions that handle certain business logic. I will give a brief descrition of a couple*.


## index
 The index route of the application is where active listings are displayed. These are auctions of products that have not been closed yet. The database is queried for required data and is rendered on the page upon request. The index view function does not require users to be logged in hence is not decorated by the `login_required` decorator.


## login and reguster
 The login and register view functions does exactly what their name says. The `login` function logs a user in and starts a session.The `register` function on the other hand add a new user acount and logs the user in,redirecting to the index route.

## logout
 Logs a user out and ends the session.

## create
 This view function handles the form submitted by a user to add a new active listing. Form data is recieved , checked and data added to the database. Upon success, a new active listing is added can be seen on the the index page.


## listing_info
 The function renders a template when a listing on the index page or watchlist is clicked. It displays more information about the listing, such as the current price or leading bid if any, date it was listed  etc. This route handler  does not require users to be logged in but certain operations on the page such as adding an item to watchlist, adding a comment or bidding on item require login autentication .


## new_bid
 Recieves a form with a new bid  on a listing, generally checks if the  bid is high enough and if it is  the bid is added as a new bid on the item and the current price of the item is changed. If the price is lower than the leading bid or price, error is thrown and user is notified. This fucntion is decrorated and required login.

## add_comment
 Adds a comment to a particular listing. Function is decrorated and requires login


## add_to_watchlist
 Adds the listing item to a users watchlist. Items can only be  added to watchlist once for a user as if you try to add the same item again you're notifed its already in your watchlist. Also items in a users watchlist can be removed from the watchlist page.


## close_auction
The close auction function is decorated and requires login, additionally it is only available to a user who owns the listing or a user who created the listing. Other users upon visiting a listing if logged in find the close auction buttton absent. The owner of the auction on the other hand has access to it and can close the auction and render it inactive by clicking the button.

## categories
 when creating or posting  a listing, users are optionally required to provide a category the listing belongs in. Listings that have their categories provided can be accesed from the categories page. It shows all available categories of lisitings and if a category name is clicked, all listings under the category is presented. The function is not decrorated and  does not require login.


 # APP LOOk

- index page
![index page look](/assets/images/index.png)


- listing page
![listing page look](/assets/images/listingpage.png)

- watchlist page
![watchlsit page look](/assets/images/watchlist.png)


- listing page
![auction listing dex page look](/assets/images/listing.png)

- category page
![category page look](/assets/images/category.png)