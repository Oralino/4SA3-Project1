import pymongo
from pymongo import MongoClient

class ObjectPool:
    def __init__(self, connection_string):
        # Initializes the pool with an empty list for reusable connections
        self.connection_string = connection_string
        self.reusables = []

    def acquire(self):
        # Returns an existing connection or creates a new one if the pool is empty
        if len(self.reusables) > 0:
            return self.reusables.pop()
        return MongoClient(self.connection_string)

    def release(self, client):
        # Adds the connection back to the reusable pool
        self.reusables.append(client)
        
class ProfileModel:
    def __init__(self, pool):
        # Stores the database pool and sets up the collection reference
        self.pool = pool
        client = self.pool.acquire()
        self.collection = client.get_database("engine_optimizer_db").get_collection("game_profiles")
        self.pool.release(client)
        
    def insert_profile(self, data):
        # Inserts a new document into the MongoDB collection
        self.collection.insert_one(data)
        
    def get_all_profiles(self):
        # Retrieves all documents from the MongoDB collection
        return list(self.collection.find({}))

    def delete_profile(self, profile_game):
        # Deletes a document from the collection based on the game name
        self.collection.delete_one({"game": profile_game})
        
