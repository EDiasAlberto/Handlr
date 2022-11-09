import pymongo, os, random, datetime

#Collection of functions used to manage listings and listing information

class ListingFuncs:

    def __init__(self, databaseURL):
        self.client = pymongo.MongoClient(databaseURL)
        self.db = self.client.handlr_database
        self.collection = self.db["listings"]

    #Fetches a random set of listings
    def fetchRandomisedListings(self, limit=5):
        listings = []
        while len(listings)<limit:
            randomListing = list(self.collection.aggregate([{"$sample": {"size":1}}]))[0]
            if randomListing not in listings:
                listings.append(randomListing)
        random.shuffle(listings)
        return listings
        
    #fetches all listings for a specific user and generates HTML previews
    def generateUsrListings(self, username):
        usrListingsHTML = ""
        for listing in self.collection.find({"account":username.lower()}):
            HTML = self.generateListingPreviews(listing)
            usrListingsHTML += HTML
        return usrListingsHTML

    #fetches specfiic listing from database from its title
    def fetchSpecificListing(self, title):
        listing = self.collection.find_one({"title":title})
        return listing

    #Fetches all listings that have titles matching a search query
    def fetchSimilarListing(self, query):
        listing = list(self.collection.find({"title" : {"$regex" : query, "$options" : "i"}}))[0:10]
        return listing

    #Produces a listing based on inputted information and uploads to database
    def createListing(self, usr, imgURL, title, desc, quality, price):
        listing = {
            "account" : usr,
            "title" : title,
            "imageURL" : imgURL,
            "description" : desc,
            "price" : price,
            "dateCreated" : datetime.datetime.now()
        }
        self.collection.insert_one(listing)

    #Produces html formatted rows of item previews
    def generateListingPreviews(self, listing):
        listingHTML = f"""
        <div class='listingPreviewRow'>
            <div>
                <img src={listing["imageURL"]} alt='Product Image' class='listingImgPreview'>
            </div>
            <div>
                <a class='listingPreviewLinks' href='/listing/{listing["title"]}'>{listing["title"]}</a>
                <h3 style='vertical-align:top;'>£{listing["price"]}</h3>
                <h4 style='vertical-align:top;'>{listing["account"].capitalize()}</h4>
            </div>
        </div>
        """
        return listingHTML