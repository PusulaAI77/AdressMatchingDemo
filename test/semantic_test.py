from sentence_transformers import SentenceTransformer, util

# Türkçe BERT modeli
model = SentenceTransformer("dbmdz/bert-base-turkish-cased")

# Metinler
text1 = "TBMM Binası"
text2 = "Türkiye Büyük Millet Meclisi"
text3 = "Örnek OSB"
text4 = "Örnek Organize Sanayi Bölgesi"
text5 = "PTT"
text6 = "Pijama Terlik Televizyon"

# Metinleri vektöre dönüştür
vec1 = model.encode(text1, convert_to_tensor=True)
vec2 = model.encode(text2, convert_to_tensor=True)
vec3 = model.encode(text3,convert_to_tensor = True)
vec4 = model.encode(text4,convert_to_tensor = True)
vec5 = model.encode(text5,convert_to_tensor = True)
vec6 = model.encode(text6,convert_to_tensor = True)


# Cosine benzerliği hesapla
score = util.cos_sim(vec1, vec2)
score2 = util.cos_sim(vec3,vec4)
score3 = util.cos_sim(vec5,vec6)

print(f"Benzerlik skoru: {score.item():.4f}")
print(f"Benzerlik skoru: {score2.item():.4f}")
print(f"Benzerlik skoru: {score3.item():.4f}")

# Eğer skor 0.85 gibi yüksek çıkarsa, iki metin anlamca çok yakın demektir.