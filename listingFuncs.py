import pymongo, os, random

def databaseConnection():
    databaseURL = os.getenv("databaseURL")
    client = pymongo.MongoClient(databaseURL)
    db = client.handlr_database
    collection = db["listings"]
    return collection

def fetchRandomisedListings():
    collection=databaseConnection()
    listings=[]
    for listing in collection.find():
        listings.append(listing)
    random.shuffle(listings)
    return listings
     
def generateUsrListings(username):
    collection=databaseConnection()
    usrListingsHTML = ""
    for listing in collection.find({"account":username.lower()}):
        HTML = generateListingPreviews(listing)
        usrListingsHTML += HTML
    return usrListingsHTML

def fetchSpecificListing(title):
    collection=databaseConnection()
    listing = collection.find_one({"title":title})
    return listing


def generateListingPreviews(listing):
    listingHTML = f"""
    <div class='listingPreviewRow'>
        <img src={listing["imageURL"]} alt='Product Image' class='listingImgPreview'>
        <div>
            <a style='vertical-align:top; text-decoration:none; font-size:larger; font-weight:bolder;' href='/listing/{listing["title"]}'>{listing["title"]}</a>
            <h3 style='vertical-align:top;'>£{listing["price"]}</h3>
            <h4 style='vertical-align:top;'>{listing["account"].capitalize()}</h4>
        </div>
    </div>
    """
    return listingHTML