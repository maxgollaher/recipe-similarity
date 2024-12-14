from config import db_password
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = f"mongodb+srv://maxgollaher:{db_password}@cluster0.3z4bn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))


class Client:
    def __init__(self, db_name, collection_name):
        self.db = client[db_name]
        self.collection = self.db[collection_name]

    def ping(self):
        try:
            client.admin.command('ping')
            return "Pinged your deployment. You successfully connected to MongoDB!"
        except Exception as e:
            return e


db_client = Client('recipe-collection', 'recipes')
