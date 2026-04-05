import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

print("Step 1: Loading environment variables...")
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("ERROR: MONGO_URI is missing. Check your .env file.")
    exit()

print("Step 2: Attempting to connect to MongoDB...")
try:
    # Uses a 5-second timeout instead of the default 30 seconds
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Forces a connection test
    client.admin.command('ping')
    print("SUCCESS: Connected to MongoDB Atlas.")
    
    print("Step 3: Attempting to insert test data...")
    db = client.get_database("engine_optimizer_db")
    collection = db.get_collection("game_profiles")
    
    test_data = {"game": "Test Game", "gpu": "Test GPU", "ini_data": "Test Data"}
    collection.insert_one(test_data)
    
    print("SUCCESS: Test data inserted. Check your Atlas dashboard and click refresh.")
    
except ServerSelectionTimeoutError:
    print("\nERROR: Network Timeout. Your IP address is blocked by the Atlas firewall.")
except Exception as e:
    print(f"\nERROR: An unexpected issue occurred: {e}")
finally:
    if 'client' in locals():
        client.close()