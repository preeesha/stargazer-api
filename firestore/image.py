import pymongo
from pprint import pprint
import json

client = pymongo.MongoClient("mongodb+srv://prishapg101:wLRnmehVtgWE3D3h@cluster0.3il6oey.mongodb.net/")

db = client["florence"]

Products_coll = db["products"]

Products = Products_coll.find({})

productImages=[]

for product in Products:
    productImage={}
    productImage["id"]=product["id"]
    productImage["images"]=product["images"]
    productImages.append(productImage)
    
    
for productImage in productImages:
    pprint(productImage)
    
with open("imageData.txt", 'w+') as f:
     json.dump(productImages,f)
        

