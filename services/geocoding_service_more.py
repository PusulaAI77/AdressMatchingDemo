cache = {}

import requests

API_KEY = "***"
BASE_URL = "https://api.geoapify.com/v1/geocode/search"

cache = {}

def get_coordinates_from_api(address):
    params = {
        "text": address,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    results = []
    if "features" in data:
        for feature in data["features"]:
            lat = feature["geometry"]["coordinates"][1]
            lon = feature["geometry"]["coordinates"][0]
            confidence = feature["properties"]["rank"]["confidence"]
            results.append({
                "lat": lat,
                "lon": lon,
                "confidence": confidence
            })
    
    # Confidence'e göre sırala
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results

def get_coordinates(address):
    if address in cache:
        print(f"Önbellekten alındı: {address}")
        return cache[address]

    results = get_coordinates_from_api(address)
    if results:
        cache[address] = results
        return results
    return []

def print_results(address, results):
    print(f"Adres: {address}")
    print("-" * 33)
    for i, r in enumerate(results, start=1):
        print(f"{i}) Enlem: {r['lat']}, Boylam: {r['lon']}, Güven: %{r['confidence']*100:.0f}")

if __name__ == "__main__":
    adres1 = "İstanbul beylikdüzü"
    sonuc = get_coordinates(adres1)
    print_results(adres1, sonuc)
