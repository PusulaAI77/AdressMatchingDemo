import requests

# İl adlarını plaka koduna çeviren dict
PLAKA_MAP = {
    "ADANA": 1,
    "ADIYAMAN": 2,
    "AFYON": 3,
    "AĞRI": 4,
    "AMASYA": 5,
    "ANKARA": 6,
    "ANTALYA": 7,
    "ARTVİN": 8,
    "AYDIN": 9,
    "BALIKESİR": 10,
    "BİLECİK": 11,
    "BİNGÖL": 12,
    "BİTLİS": 13,
    "BOLU": 14,
    "BURDUR": 15,
    "BURSA": 16,
    "ÇANAKKALE": 17,
    "ÇANKIRI": 18,
    "ÇORUM": 19,
    "DENİZLİ": 20,
    "DİYARBAKIR": 21,
    "EDİRNE": 22,
    "ELAZIĞ": 23,
    "ERZİNCAN": 24,
    "ERZURUM": 25,
    "ESKİŞEHİR": 26,
    "GAZİANTEP": 27,
    "GİRESUN": 28,
    "GÜMÜŞHANE": 29,
    "HAKKARİ": 30,
    "HATAY": 31,
    "ISPARTA": 32,
    "MERSİN": 33,
    "İSTANBUL": 34,
    "İZMİR": 35,
    "KARS": 36,
    "KASTAMONU": 37,
    "KAYSERİ": 38,
    "KIRKLARELİ": 39,
    "KIRŞEHİR": 40,
    "KOCAELİ": 41,
    "KONYA": 42,
    "KÜTAHYA": 43,
    "MALATYA": 44,
    "MANİSA": 45,
    "KAHRAMANMARAŞ": 46,
    "MARDİN": 47,
    "MUĞLA": 48,
    "MUŞ": 49,
    "NEVŞEHİR": 50,
    "NİĞDE": 51,
    "ORDU": 52,
    "RİZE": 53,
    "SAKARYA": 54,
    "SAMSUN": 55,
    "SİİRT": 56,
    "SİNOP": 57,
    "SİVAS": 58,
    "TEKİRDAĞ": 59,
    "TOKAT": 60,
    "TRABZON": 61,
    "TUNCELİ": 62,
    "ŞANLIURFA": 63,
    "UŞAK": 64,
    "VAN": 65,
    "YOZGAT": 66,
    "ZONGULDAK": 67,
    "AKSARAY": 68,
    "BAYBURT": 69,
    "KARAMAN": 70,
    "KIRIKKALE": 71,
    "BATMAN": 72,
    "ŞIRNAK": 73,
    "BARTIN": 74,
    "ARDAHAN": 75,
    "IĞDIR": 76,
    "YALOVA": 77,
    "KARABÜK": 78,
    "KİLİS": 79,
    "OSMANİYE": 80,
    "DÜZCE": 81
}

def normalize_name(name):
    """İsimleri küçük harfe çevir, boşlukları temizle ve 'mah', 'mahalle' eklerini kaldır"""
    name = name.lower().strip()
    name = name.replace("mahalle", "").replace("mah", "").replace(".", "").strip()
    return name

def get_postal_code(province_name, district_name, neighborhood_name):
    province_upper = province_name.upper()
    plaka = PLAKA_MAP.get(province_upper)
    if not plaka:
        print(f"Plaka bulunamadı: {province_name}")
        return None

    url = f"https://api.zumbo.net/postakodu/il/{plaka}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print("API çağrısı başarısız")
        return None

    data = resp.json().get("postakodu", [])
    district_norm = normalize_name(district_name)
    neighborhood_norm = normalize_name(neighborhood_name)

    for item in data:
        item_district = normalize_name(item["ilce"])
        item_neighborhood = normalize_name(item["mahalle"])
        if district_norm in item_district and neighborhood_norm in item_neighborhood:
            return item["pk"]  # sadece posta kodunu döndür

    # Eğer tam eşleşme yoksa ilçe bazlı fallback
    for item in data:
        item_district = normalize_name(item["ilce"])
        if district_norm in item_district:
            return item["pk"]

    print(f"Eşleşen posta kodu bulunamadı: {province_name}, {district_name}, {neighborhood_name}")
    return None

# Test
#if __name__ == "__main__":
#    province = "Adana"
#    district = "Aladağ"
#    neighborhood = "Başpınar Mah"
#    result = get_postal_code(province, district, neighborhood)
#    print("Postal code:", result)
