from pymongo import MongoClient
class Database():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')