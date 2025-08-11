import requests

BASE_URL = "https://turkiyeapi.dev/api/v1"

def get_province(province_name):
    url = f"{BASE_URL}/provinces"
    params = {"name": province_name, "activatePostalCodes": "true"}
    resp = requests.get(url, params=params)
    data = resp.json()
    if data.get("status") == "OK" and data.get("data"):
        for province in data["data"]:
            if province["name"].lower() == province_name.lower():
                return province
    return None

def get_district(province_id, district_name):
    url = f"{BASE_URL}/districts"
    params = {"provinceId": province_id, "name": district_name, "activatePostalCodes": "true"}
    resp = requests.get(url, params=params)
    data = resp.json()
    if data.get("status") == "OK" and data.get("data"):
        for district in data["data"]:
            if district["name"].lower() == district_name.lower():
                return district
    return None

def get_neighborhood(province_id, district_id, neighborhood_name):
    url = f"{BASE_URL}/neighborhoods"
    params = {
        "provinceId": province_id,
        "districtId": district_id,
        "name": neighborhood_name
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    if data.get("status") == "OK" and data.get("data"):
        for nb in data["data"]:
            if nb["name"].lower() == neighborhood_name.lower():
                return nb
    return None

def get_postal_code(province_name, district_name, neighborhood_name=None):
    province = get_province(province_name)
    if not province:
        print(f"Province '{province_name}' not found.")
        return None

    district = get_district(province["id"], district_name)
    if not district:
        print(f"District '{district_name}' not found in province '{province_name}'.")
        return None

    if neighborhood_name:
        neighborhood = get_neighborhood(province["id"], district["id"], neighborhood_name)
        if not neighborhood:
            print(f"Neighborhood '{neighborhood_name}' not found in district '{district_name}'.")
            return None
        # Mahalle için şu anda postal code olmayabilir, None dönebilir
        postal_code = neighborhood.get("postalCode")
        return {
            "province": province_name,
            "province_id": province["id"],
            "district": district_name,
            "district_id": district["id"],
            "neighborhood": neighborhood_name,
            "postal_code": postal_code
        }
    else:
        # Mahalle verilmediyse sadece il ve ilçe posta kodu
        return {
            "province": province_name,
            "province_id": province["id"],
            "district": district_name,
            "district_id": district["id"],
            "neighborhood": None,
            "postal_code": district.get("postalCode")  # İlçe posta kodu
        }
 # test
if __name__ == "__main__":
    province = "Adana"
    district = "Aladağ"
    neighborhood = "Başpınar"  # Mahalle adı ver

    result = get_postal_code(province, district, neighborhood)
    print("Sonuç:", result)
