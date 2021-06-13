import pymongo, os, random

def fetchRandomListing():
    databaseURL = os.getenv("databaseURL")
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["listings"]
    listings=[]
    for listing in collection.find():
        listings.append(listing)
    listing = random.choice(listings)
    return listing

def fetchRandomisedListings():
    databaseURL = os.getenv("databaseURL")
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["listings"]
    listings=[]
    for listing in collection.find():
        listings.append(listing)
    random.shuffle(listings)
    return listings
     
def generateUsrListings(username):
    databaseURL = os.getenv("databaseURL")
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["listings"]
    usrListingsHTML = ""
    for listing in collection.find({"account":username.lower()}):
        HTML = generateListingPreviews(listing)
        usrListingsHTML += HTML
    return usrListingsHTML



def generateListingPreviews(listing):
    listingHTML = f"""
    <div class='listingPreviewRow'>
        <img src={listing["imageURL"]} alt='Product Image' class='listingImgPreview'>
        <div>
            <h3 style='vertical-align:top;'>{listing["title"]}</h2>
            <h3 style='vertical-align:top;'>£{listing["price"]}</h3>
            <h4 style='vertical-align:top;'>{listing["account"].capitalize()}</h4>
        </div>
    </div>
    """
    return listingHTML