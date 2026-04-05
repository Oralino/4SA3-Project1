from models.database_model import ProfileModel
from models.maps_api import MapsAPIClient
from strategies.export_strategy import JsonExportStrategy

class AppController:
    def __init__(self, db_pool, api_key):
        # Initializes the model layers with the database pool and API key
        self.model = ProfileModel(db_pool)
        self.api = MapsAPIClient(api_key)
        self.export_strategy = JsonExportStrategy()

    def save_profile(self, game, gpu, ini_data):
        # Formats the data and passes it to the database model
        data = {
            "game": game,
            "gpu": gpu,
            "ini_data": ini_data
        }
        print(f"DEBUG: Button clicked. Sending this exact payload to model: {data}")
        self.model.insert_profile(data)

    def load_profiles(self):
        # Fetches profiles from the database
        return self.model.get_all_profiles()

    def delete_profile(self, game_name):
        # Instructs the database model to remove a specific profile
        self.model.delete_profile(game_name)

    def fetch_shops(self, query):
        # Requests local shop data from the API model
        return self.api.search_shops(query)