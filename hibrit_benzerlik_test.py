from thefuzz import fuzz
import jellyfish

def adres_benzerlik(adres1, adres2):
    """
    Hibrit Adres Benzerlik Fonksiyonu
    Ağırlıklar:
        Token Sort Ratio -> %50
        Partial Ratio    -> %30
        Jaro-Winkler     -> %20
    """
    # Sözcüksel benzerlik skorları
    token_sort = fuzz.token_sort_ratio(adres1, adres2)      # %50
    partial = fuzz.partial_ratio(adres1, adres2)            # %30
    jaro = jellyfish.jaro_winkler_similarity(adres1, adres2) * 100      # %20 (0-1 arası → 0-100 arası)

    # Ağırlıklı ortalama
    final_score = (token_sort * 0.50) + (partial * 0.30) + (jaro * 0.20)
    return round(final_score, 2)

# Test örnekleri
adres_a = "Atatürk Mahallesi 15 Sokak"
adres_b = "15 Sk. Atatürk Mahallesi"
adres_c = "Ataturk Mah. 15 Sok."
adres_d = "ataturk 15 sok."

# print(adres_benzerlik(adres_a, adres_b))  # Yüksek 
# print(adres_benzerlik(adres_a, adres_c))  # Orta-yüksek 
# print(adres_benzerlik(adres_a,adres_d))   # düşük

