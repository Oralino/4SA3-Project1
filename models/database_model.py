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
        # Stores the database pool reference for later use
        self.pool = pool

    def insert_profile(self, data):
        # Acquires an active connection just for saving data
        client = self.pool.acquire()
        collection = client.get_database("engine_optimizer_db").get_collection("game_profiles")
        
        collection.insert_one(data)
        print("SUCCESS: Profile saved to MongoDB cluster.")
        
        # Returns the connection to the pool
        self.pool.release(client)

    def get_all_profiles(self):
        # Acquires an active connection just for reading data
        client = self.pool.acquire()
        collection = client.get_database("engine_optimizer_db").get_collection("game_profiles")
        
        profiles = list(collection.find({}))
        print(f"SUCCESS: Loaded {len(profiles)} profiles from MongoDB cluster.")
        
        # Returns the connection to the pool
        self.pool.release(client)
        return profiles

    def delete_profile(self, profile_game):
        # Acquires an active connection just for deleting data
        client = self.pool.acquire()
        collection = client.get_database("engine_optimizer_db").get_collection("game_profiles")
        
        collection.delete_one({"game": profile_game})
        print(f"SUCCESS: Deleted profile for {profile_game} from MongoDB cluster.")
        
        # Returns the connection to the pool
        self.pool.release(client)