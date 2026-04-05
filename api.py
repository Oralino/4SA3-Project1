import requests
API_KEY = "YOUR_GOOGLE_API_KEY"

def find_local_pc_shops(search_query="PC repair shop near me"):
    # Google Maps Text Search API endpoint
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        "query": search_query,
        "key": API_KEY
    }
    
    try:
        print(f"Pinging Google Maps API for: '{search_query}'...")
        # Establish connection to the third-party web service
        response = requests.get(url, params=params)
        data = response.json()
        
        # Retrieve and manipulate the data
        if response.status_code == 200 and data.get("results"):
            print("Successfully retrieved data from Google Maps API!\n")
            print("Top 3 PC Shops found:")
            
            # Loop through and display the top 3 results
            for i, shop in enumerate(data["results"][:3], 1):
                name = shop.get('name')
                address = shop.get('formatted_address')
                print(f"{i}. {name} - {address}")
        else:
            print("No results found. Check your API key or query.")
            
    except Exception as e:
        print("Failed to connect to the API:", e)

if __name__ == "__main__":
    find_local_pc_shops()