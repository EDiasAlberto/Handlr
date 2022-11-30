from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os, pymongo, random
import verifyFuncs, listingFuncs, imgFuncs, questionFuncs, forms

load_dotenv()
flaskKey = os.getenv("flaskKey")
databaseURL = os.getenv("databaseURL")
imgSiteURL = os.getenv("imgSiteURL")

listingFuncs = listingFuncs.ListingFuncs(databaseURL)
verification = verifyFuncs.VerifyFuncs(databaseURL)
imgFuncs = imgFuncs.ImgFuncs(imgSiteURL)
questionFuncs = questionFuncs.QuestionFuncs(databaseURL)

webapp = Flask(__name__)
webapp.config['UPLOAD_FOLDER'] = "uploads/"

@webapp.route("/", methods=['GET', 'POST'])
def login():
    error = None
    form = forms.LoginForm()
    if request.method=="POST":
        username = form.username.data
        password = form.password.data
        valid = verification.verifyUsr(username, password)
        if not valid:
            error = 'Invalid Credentials. Please try again.'
        else:
            session["username"]=username
            return redirect(url_for("index"))
    return render_template('login.html', error=error, form=form)

@webapp.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        error = verification.newUsr(username, password, confirmPassword)
        if error==None:
            return redirect(url_for("login"))
        flash(error)
    return render_template('register.html')


@webapp.route("/home")
def index():
    listingsHTML =""
    if "username" in session:
        randomListings = listingFuncs.fetchRandomisedListings()
        for i in range(5):
            listingsHTML+=listingFuncs.generateListingPreviews(randomListings[i])
        usrListingsHTML = listingFuncs.generateUsrListings(session["username"])
        return render_template("index.html", publicListings=listingsHTML, usrListings=usrListingsHTML, classHome="active")
    else:
        return redirect(url_for("login"))

@webapp.route("/listings")
def listings():
    if "username" in session:
        listingsHTML = listingFuncs.generateUsrListings(session["username"])
        return render_template("listings.html", usrListings = listingsHTML, classListings="active")

    return redirect(url_for("login"))

@webapp.route("/listing/<listingTitle>")
def specificListing(listingTitle):
    if "username" in session:
        listingOwner = request.args.get("account")
        listing = listingFuncs.fetchSpecificListing(listingTitle, listingOwner)
        isOwner = listingOwner.lower()==session["username"].lower()
        questions = questionFuncs.fetchQuestions(listingTitle, listingOwner)
        if int(listing["price"])==listing["price"]:
            listing["price"] = str(listing["price"]) + "0"
        print(isOwner)
        return render_template("specificListing.html",listing = listing, questions=questions, isOwner=isOwner)
    return redirect(url_for("login"))

@webapp.route("/purchase/<listingTitle>", methods=["POST"])
def purchaseListing(listingTitle):
    if "username" in session:
        listingOwner = request.args.get("account")
        listing = listingFuncs.fetchSpecificListing(listingTitle, listingOwner)
        return f"<p>YOU HAVE PURCHASED ONE {listing['title']} at price £{listing['price']}!</p>"

@webapp.route("/generateLabel/<ListingTitle>", methods=["POST"])
def generateLabel(listingTitle):
    if "username" in session:
        listingOwner = request.args.get("account")
        if listingOwner==session["username"]:
            label = listingFuncs.generateLabel(listingTitle, listingOwner)
            listingFuncs.saveLabel(label)
            return render_template("specificListing.html", listingTitle=listingTitle, listingOwner=listingOwner)

@webapp.route("/createListing", methods=["GET", "POST"])
def createListing():
    if request.method=="POST":
        file = request.files["image"]
        imgURL = imgFuncs.imgUpload(file, webapp.config['UPLOAD_FOLDER'], session["username"].lower())
        title = request.form["title"]
        desc = request.form["description"]
        quality = request.form.get("quality")
        price = float(request.form["price"])
        isValidListing = listingFuncs.createListing(session["username"].lower(), imgURL, title, desc, quality, price)
        if not isValidListing:
            flash("Error! You already have a listing with this name")
            return render_template("createListing.html")
        
        return redirect(url_for("specificListing", listingTitle=title, account = session["username"]))

    else:
        return render_template("createListing.html")

#Handles search page rendering and logic
@webapp.route("/search", methods=["GET","POST"])
def search():
    #Checks if the user has submitted a search query
    if request.method=="POST":
        listingsHTML=""
        SortingKeys = {"Relevance" : None, "Quality" : "quality", "Title" : "title", 
        "Newest First" : "dateCreated", "Price (High to Low)" : "price", "Price (Low to High)" : "price"}
        #It then fetches all listings matching this query
        searchResults = listingFuncs.fetchSimilarListing(request.form["query"])
        #Then it fetches the desired sorting of the listing items (default is similarity to query)
        sortValue = request.form.get("sort")
        if SortingKeys[sortValue] is not None:
            #This then sorts the fetched listings by the desired attribute, in descending/ascending order 
            if sortValue=="Price (High to Low)":
                searchResults = sorted(searchResults, key= lambda x: x[SortingKeys[sortValue]], reverse=True)
            else:
                searchResults=sorted(searchResults, key= lambda x: x[SortingKeys[sortValue]])
        #Then HTML text is generated to render the sorted search results 
        for listing in searchResults:
            listingsHTML+=listingFuncs.generateListingPreviews(listing)
        #Then the search page is refreshed to display the search results, sorted appropriately
        return render_template("search.html", searchResults = listingsHTML, classSearch="active", choice=sortValue)
    #If the user did not search anything yet, it only displays the search bar and an empty remainder of the page
    return render_template("search.html", classSearch="active", choice="Relevance")


@webapp.route("/account", methods=["GET", "POST"])
def account():
    if "username" in session:
        if request.method=="POST":
            isValidChange = verification.updatePass(session["username"].lower(), request.form["oldPassword"], request.form["newPassword"], request.form["confirmPassword"])
            print(isValidChange)
            if not isValidChange:
                return render_template("account.html", classAccount="active", error="Error! Invalid username and/or password.")
            return render_template("account.html", classAccount="active", success="Successfully updated password.")
        else:
            return render_template("account.html")
    return redirect(url_for("login"))

@webapp.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("login"))

@webapp.route("/secret/")
def secretPage():
    return "Congratulations, you have found the secret hidden webpage that nobody knows about."

@webapp.route("/secret/<name>/")
def secretName(name):
    return f"Congratulations, {name}, you have found the secret hidden webpage that nobody knows about."

@webapp.route("/test")
def test():
    return render_template("testPage.html")

@webapp.route("/newmenu")
def newMenu():
    return render_template("menubar.html", classSearch="active")

if __name__=="__main__":
    webapp.secret_key = flaskKey
    #listingFuncs.addAField("isSold", False)
    webapp.run(port=4200, debug=True)
