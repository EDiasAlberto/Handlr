import pymongo, os, random

#Collection of functions used to manage listings and listing information

class ListingFuncs:

    def __init__(self, databaseURL):
        self.client = pymongo.MongoClient(databaseURL)
        self.db = self.client.handlr_database
        self.collection = self.db["listings"]

    #Fetches a random set of listings
    def fetchRandomisedListings(self, limit=5):
        listings=[listing for listing in self.collection.find(limit=limit)]
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

    #Produces html formatted rows of item previews
    def generateListingPreviews(self, listing):
        listingHTML = f"""
        <div class='listingPreviewRow'>
            <img src={listing["imageURL"]} alt='Product Image' class='listingImgPreview'>
            <div>
                <a class='listingPreviewLinks' href='/listing/{listing["title"]}'>{listing["title"]}</a>
                <h3 style='vertical-align:top;'>£{listing["price"]}</h3>
                <h4 style='vertical-align:top;'>{listing["account"].capitalize()}</h4>
            </div>
        </div>
        """
        return listingHTML