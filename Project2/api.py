import requests

def get_elevation(latitude, longitude, api_key = "<api_key>"):
    base_url = "https://maps.googleapis.com/maps/api/elevation/json"
    params = {
        "locations": f"{latitude},{longitude}",
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            elevation = data["results"][0]["elevation"]
            return elevation
            # print(f"{elevation}")
        else:
            print("Data error")
    else:
        print("Failed request")

#if __name__ == "__main__":
    # api_key = "AIzaSyD9BRgtHmmIYyqRmy92puu3U6KVd9W3BqI"
    # latitude = 33.4219999  
    # longitude = 93.0840575 
    # get_elevation(latitude, longitude, api_key)
