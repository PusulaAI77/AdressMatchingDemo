cache = {}

import requests

API_KEY = "8054cf6228174d6b964ea27d622bf534"
BASE_URL = "https://api.geoapify.com/v1/geocode/search"

# postmande yaptığımız işlemin burada kodu var
def get_coordinates_from_api(address):
    params = {
        "text": address,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "features" in data and len(data["features"]) > 0:
        lat = data["features"][0]["geometry"]["coordinates"][1]
        lon = data["features"][0]["geometry"]["coordinates"][0]
        return lat, lon
    return None, None

# adresi önce cache de arayacağız yoksa api ye istek atacağız 

def get_coordinates(address):
    if address in cache:
        print("Önbellekten alındı:", address)
        return cache[address]

    # API’den çek
    lat, lon = get_coordinates_from_api(address)
    if lat and lon:
        cache[address] = (lat, lon)  # Cache'e ekle
        return lat, lon
    return None, None

#test edelim
if __name__ == "__main__":
    adres1 = "İstanbul beylikdüzü"
    print(get_coordinates(adres1))  # İlk sefer API'den gelir
    print(get_coordinates(adres1))  # İkinci sefer cache'ten gelir
