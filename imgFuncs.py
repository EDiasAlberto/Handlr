from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import requests, os, base64

class ImgFuncs:
    def __init__(self, imgSiteURL):
        self.URL = imgSiteURL

    def imgUpload(self, file, folder, username):
        path = os.path.join(folder, f"{username}.png")
        file.save(path)
        with open(path, "rb") as img:
            encoded = base64.b64encode(img.read())
        myobj = {'image': encoded}

        x = requests.post(self.URL, data = myobj)
        responseDict = x.json()
        os.remove(path)
        return responseDict["data"]["display_url"]

