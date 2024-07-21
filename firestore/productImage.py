import os
import requests
import firebase_admin
from firebase_admin import credentials, storage
import pymongo
from pymongo.errors import PyMongoError
from pprint import pprint
import json


# Initialize Firebase Admin SDK with service account key
cred = credentials.Certificate("./firestore/firestoreSDK.json")
firebase_admin.initialize_app(cred, {"storageBucket": "florence-preeesha.appspot.com"})

# Get a reference to the Firebase Storage service
bucket = storage.bucket()


def download_image(url, local_filename):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Save the image data to a local file
        with open(local_filename, "wb") as f:
            f.write(response.content)
        print("Image downloaded successfully")
    else:
        print("Failed to download image")


def upload_image(local_filename, destination_blob_name):
    # Upload the image to Firebase Storage
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_filename)

    print("Image uploaded to Firebase Storage")
    storage_ref = storage.bucket().blob(destination_blob_name)

    # Get the download URL
    url = storage_ref.public_url

    return url


def uploadImageOnFirestore(img_url: str, name: str):
    # URL of the image to download
    image_url = img_url

    # Local filename to save the downloaded image
    local_filename = "image.jpg"

    # Destination path in Firebase Storage to upload the image
    destination_blob_name = f"{name}"

    # Download the image from the URL
    download_image(image_url, local_filename)

    # Upload the downloaded image to Firebase Storage
    url = upload_image(local_filename, destination_blob_name)

    # Delete the local image file after uploading
    os.remove(local_filename)

    return url


# url = uploadImageOnFirestore("https://google.com/favicon.ico", "favicon.ico")
# print(url)

client = pymongo.MongoClient(
    "mongodb+srv://prishapg101:wLRnmehVtgWE3D3h@cluster0.3il6oey.mongodb.net/"
)


def change_url_image_mongo():
    try:
        db = client["florence"]

        products_coll = db["products_1"]

        products_cursor = products_coll.find({})
        products = tuple(products_cursor)[1:]

        for product in products:
            print(product["id"])
            Product_images = product["images"]

            new_product_images_url = []
            for product_image_url in Product_images:
                new_img_url = uploadImageOnFirestore(
                    product_image_url, product_image_url
                )
                new_product_images_url.append(new_img_url)

            products_coll.update_one(
                {"id": product["id"]}, {"$set": {"images": new_product_images_url}}
            )

    except PyMongoError as e:
        print("the error occured is ", e)


change_url_image_mongo()
