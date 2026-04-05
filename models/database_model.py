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
        
        # Connects to the engine optimizer database
        self.collection = client.get_database("engine_optimizer_db").get_collection("game_profiles")
        
        self.pool.release(client)

    def insert_profile(self, data):
        # Inserts a new document into the MongoDB collection and prints a terminal confirmation
        print("Testing mongo connection...")
        self.collection.insert_one(data)
        print("SUCCESS: Profile saved to MongoDB cluster.")

    def get_all_profiles(self):
        # Retrieves all documents from the MongoDB collection and prints a terminal confirmation
        profiles = list(self.collection.find({}))
        print(f"SUCCESS: Loaded {len(profiles)} profiles from MongoDB cluster.")
        return profiles

    def delete_profile(self, profile_game):
        # Deletes a document from the collection and prints a terminal confirmation
        self.collection.delete_one({"game": profile_game})
        print(f"SUCCESS: Deleted profile for {profile_game} from MongoDB cluster.")
        
