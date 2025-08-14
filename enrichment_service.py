from matching_service import match_address
from services.postalcode_service import get_postal_code
from services.geocoding_service import get_coordinates
from services.parsing_service import parse_address

def enrich_address(input_address: str):
    # 1- En iyi eşleşen adresi bul
    match_result = match_address(input_address)

    if not match_result["matched_address"]:
        return {"error": "Adres bulunamadı"}

    # 2- Eşleşen adresi parçala
    parsed = parse_address(match_result["matched_address"])

    # Basitçe entity'leri ayıklayalım:
    province = None
    district = None
    neighborhood = None

    for entity in parsed["entities"]:
        if entity["entity_group"] == "PROVINCE":  # Veya senin modelde il için ne varsa
            province = entity["word"]
        elif entity["entity_group"] == "DISTRICT":
            district = entity["word"]
        elif entity["entity_group"] == "NEIGHBORHOOD":
            neighborhood = entity["word"]

    # Eğer parse’dan çıkmadıysa default olarak eşleşen adresin içinde isimlerden alabiliriz:
    if not province:
        # Örnek: "İstanbul Kadıköy ..." gibi
        # Daha gelişmiş parse lazım ama şimdilik None bırakıyoruz
        province = None
    if not district:
        district = None
    if not neighborhood:
        neighborhood = None

    # 3- Postalcode servisinden bilgi al
    postal_data = None
    if province and district:
        postal_data = get_postal_code(province, district, neighborhood)

    # 4- Koordinat al
    lat, lon = get_coordinates(match_result["matched_address"])

    # 5- Sonuçları toparla
    result = {
        "matched_address": match_result["matched_address"],
        "fuzzy_score": match_result["fuzzy_score"],
        "semantic_score": match_result["semantic_score"],
        "final_score": match_result["final_score"],
        "postal_data": postal_data,
        "coordinates": {"lat": lat, "lon": lon}
    }

    return result


if __name__== "__main__":
    input_address = "İstanbul Kadıköy Bahariye Mahallesi 12. Sokak"
    enriched = enrich_address(input_address)
    print("Enriched address data:")
    print(enriched)