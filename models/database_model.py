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