# benzerlik_test.py

from thefuzz import fuzz
import jellyfish

# Test çiftleri
pairs = [
    ("Atatürk Blv.", "Atatürk Bulvarı"),
    ("Cumhuriyet Mah.", "Cumhuriyet Mahallesi"),
    ("İstiklal Cd", "İstiklal Caddesi"),
    ("cicek sk", "Çiçek sokak"),
]

for text1, text2 in pairs:
    print(f"---\n'{text1}' <-> '{text2}'")

    # Fuzzy oranları
    print("ratio:", fuzz.ratio(text1, text2))
    print("partial_ratio:", fuzz.partial_ratio(text1, text2))
    print("token_sort_ratio:", fuzz.token_sort_ratio(text1, text2))

    # Jaro-Winkler
    jw_score = jellyfish.jaro_winkler_similarity(text1, text2)
    print("Jaro-Winkler:", round(jw_score * 100, 2))


  #ratio (Levenshtein Oranı)
  # İki metnin tamamını karakter karakter karşılaştırır, harf ekleme/silme/değiştirme farklarını ölçer.
  # 0 = tamamen farklı     100 = birebir aynı

  #partial_ratio
  # Metinlerin bir kısmının diğerinde ne kadar geçtiğini ölçer.Özellikle uzun metinlerde küçük parçaların eşleşmesini anlamak için kullanılır.
  # Yüksek değer (90+), bir metin diğerinin içinde geçiyorsa çıkar.
  # Tamamı farklı ama belirgin bir ortak parça varsa yine yüksek çıkar.
  
  #token_sort_ratio
  # Metindeki kelimeleri alfabetik olarak sıralar, sonra karşılaştırır.
  # Kelime sırası farklı olsa bile yüksek skor verebilir.
  # Adres gibi kelime sırası değişebilen alanlarda çok yararlı.
  # Yüksek değer (85+) benzerlik gösterir.

  #Jaro-Winkler
  # Karakterlerin sırasına ve benzer harf gruplarına bakar, yazım hatalarını tolere eder.
  # Özellikle isim, yer adı, kişi adı gibi küçük farklarda iyi çalışır.
  # 0.0 = tamamen farklı
  # 1.0 = birebir aynı
