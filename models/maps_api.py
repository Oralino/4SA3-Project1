import requests

class MapsAPIClient:
    def __init__(self, api_key):
        # Stores the API key for external requests
        self.api_key = api_key
        self.url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    def search_shops(self, query):
        # Sends a request to Google Maps and returns the top three results
        params = {
            "query": query,
            "key": self.api_key
        }
        response = requests.get(self.url, params=params)
        data = response.json()

        results = []
        if response.status_code == 200 and data.get("results"):
            for shop in data["results"][:3]:
                name = shop.get("name")
                address = shop.get("formatted_address")
                results.append(f"{name} | {address}")
        return results