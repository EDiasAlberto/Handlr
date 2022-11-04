from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os, pymongo, random
import verifyFuncs, listingFuncs, imgFuncs, forms

load_dotenv()
flaskKey = os.getenv("flaskKey")
databaseURL = os.getenv("databaseURL")
imgSiteURL = os.getenv("imgSiteURL")

listingFuncs = listingFuncs.ListingFuncs(databaseURL)
verification = verifyFuncs.VerifyFuncs(databaseURL)
imgFuncs = imgFuncs.ImgFuncs(imgSiteURL)

webapp = Flask(__name__)
webapp.config['UPLOAD_FOLDER'] = "uploads/"

@webapp.route("/", methods=['GET', 'POST'])
def login():
    error = None
    form = forms.LoginForm()
    if request.method=="POST":
        print("Submitted")
        username = form.username.data
        password = form.password.data
        print(username, password)
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

@webapp.route("/listing/<listingName>")
def specificListing(listingName):
    if "username" in session:
        listing = listingFuncs.fetchSpecificListing(listingName)
        displayHTML = f"<p>{listing['price']}<br>{listingName}</p>"
        if listing["account"]==session["username"].lower():
            displayHTML+="<br><p>You own this!</p>"
        return render_template("specificListing.html",listing = listing)
    return redirect(url_for("login"))

@webapp.route("/createListing", methods=["GET", "POST"])
def createListing():
    if request.method=="POST":
        file = request.files["image"]
        imgURL = imgFuncs.imgUpload(file, webapp.config['UPLOAD_FOLDER'], session["username"].lower())
        title = request.form["title"]
        desc = request.form["description"]
        quality = request.form.get("quality")
        price = float(request.form["price"])
        listingURL = listingFuncs.createListing(session["username"].lower(), imgURL, title, desc, quality, price)
        
        return render_template("createListing.html")

    else:
        return render_template("createListing.html")

@webapp.route("/search")
def search():
    return render_template("search.html", classSearch="active")


@webapp.route("/account")
def account():
    if "username" in session:
        return render_template("account.html", classAccount="active")
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
    webapp.run(port=4200, debug=True)
