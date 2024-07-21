from flask import Flask, request
from pymongo import MongoClient
from bson import json_util
from pprint import pprint
import json

from recommend import get_recommended_products

# db configurations

CONNECTION_STRING ="mongodb+srv://prishapg101:wLRnmehVtgWE3D3h@cluster0.3il6oey.mongodb.net/"   
client = MongoClient(CONNECTION_STRING)
source_db = client["florence"]
users_coll = source_db["users"]
products_coll = source_db["products"]



app = Flask(__name__)


@app.route("/recommended_products", methods=["POST"])
def recommend():
    data = request.get_json()
    if "email" not in data:
        return {"message": "Failed", "data": []}, 500

    email = data["email"]

    user = users_coll.find_one({"email": email})
    if not user:
        return {"message": "Failed", "data": []}, 500

    user_productsIds = user["viewHistory"]
    products = list(products_coll.find({"id": {"$in": user_productsIds}}))
    recommended_products = get_recommended_products(products)
    response = {"message": "Success", "data": recommended_products}
    response = json.loads(json_util.dumps(response))

    return response, 200


if __name__ == "__main__":
    app.run(debug=True)
    
