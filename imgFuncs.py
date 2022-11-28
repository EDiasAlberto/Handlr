from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import requests, os, base64

class ImgFuncs:
    def __init__(self, imgSiteURL):
        self.URL = imgSiteURL

    #Function to upload product images to ImgBB
    def imgUpload(self, file, folder, username):
        #First saves the image locally so it can be encoded
        path = os.path.join(folder, f"{username}.png")
        file.save(path)

        #This encodes the image file into base64 using python's base64 lib
        with open(path, "rb") as img:
            encoded = base64.b64encode(img.read())
        myobj = {'image': encoded}

        #Then it makes a POST request to ImgBB's API to upload the base64 string
        x = requests.post(self.URL, data = myobj)
        responseDict = x.json()
        
        #The saved image is deleted and then the function returns the url to the image
        #This URL can then be used when saving the listing to the database
        os.remove(path)
        return responseDict["data"]["display_url"]

