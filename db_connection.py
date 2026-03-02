import pymongo
from pymongo import MongoClient

connection_string = "YOUR_MONGO_URI"

try:
    #Connect to the cloud database
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(connection_string)
    
    server_data = client.server_info()
    
    print("Successfully connected!")
    print(f"Retrieved MongoDB Server Version: {server_data.get('version')}")

except Exception as e:
    print("Connection failed:", e)
finally:
    #Always close the connection
    if 'client' in locals():
        client.close()
        print("MongoDB connection closed.")