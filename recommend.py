from pprint import pprint
from pymongo import MongoClient
import numpy as np
from joblib import load
import random

CONNECTION_STRING ="mongodb+srv://prishapg101:wLRnmehVtgWE3D3h@cluster0.3il6oey.mongodb.net/"   
client = MongoClient(CONNECTION_STRING)
db = client["florence"]
collection = db["products"]

kmeans = load("model.bird")
all_products = list(collection.find({}))

COLORS_LIST = [
    "Orange",
    "Yellow-Orange",
    "Red",
    "Red-Orange",
    "Yellow",
    "Yellow-Green",
    "Undefined",
    "Magenta",
    "Green",
    "Purple-Magenta",
    "Purple",
    "Pink",
    "Grayish Purple",
    "Cyan",
    "Light Pink",
    "Red-Magenta",
    "Pale Pink",
    "Blue",
    "Blue-Cyan",
]


def get_recommended_products(past_products):
    frag_list = ["floral", "rosy", "orchid", "lilies"]

    feature_vectors = []
    for product in past_products:
        colors = [
            product["colors"][colour] if colour in product["colors"] else 0
            for colour in COLORS_LIST
        ]
        fragnances = [1 if frag in product["fragnance"] else 0 for frag in frag_list]
        feature_vector = colors + fragnances
        feature_vectors.append(feature_vector)

    # user_vector = np.mean(feature_vectors, axis=0)

    # Predict the cluster for the user's feature vector
    clusters = np.unique(np.array(kmeans.predict(feature_vectors)))

    print(kmeans.labels_)

    # Get indices of products in the same cluster as the user's products
    indices = []
    for i, cluster in enumerate(kmeans.labels_):
        if cluster in clusters:
            indices.append(i)

    choices = random.choices(indices, k=10)

    # Display or use the recommended products from the same cluster
    recommended_products_ids = [all_products[i]["id"] for i in choices]

    return recommended_products_ids
