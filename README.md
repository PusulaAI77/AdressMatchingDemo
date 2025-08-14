# TEKNOFEST Adres Çözümleme Hackathon'u 🚀

## Proje Özeti

Bu proje, Türkiye'deki "kirli" ve yapılandırılmamış adres metinlerini, standart ve doğrulanmış coğrafi bilgilere dönüştüren akıllı bir adres çözümleme sistemidir. E-ticaret, lojistik ve kargo sektörlerindeki adres kaynaklı sorunları çözmek için geliştirilmiştir.

## 🎯 Projenin Amacı

- Ham adres metinlerini yapılandırılmış bileşenlere ayırma (mahalle, sokak, numara, vb.)
- Yazım hatalarını ve anlamsal farklılıkları tolere eden akıllı eşleştirme
- Coğrafi koordinatlar ve posta kodu ile adres doğrulama
- Real-time API servisi ve interaktif web arayüzü

## 🏗️ Sistem Mimarisi

```
📁 ADDRESSMATCHINGDEV/
├── 📁 api/                        # FastAPI ana uygulaması
│   ├── 📁 __pycache__/           # Python cache dosyaları
│   └── main.py                   # Ana API endpoint'leri (M)
├── 📁 data/                      # Veri dosyaları ve veritabanı
├── 📁 notebooks/                 # Jupyter notebook'lar
│   ├── 📁 .ipynb_checkpoints/   # Notebook checkpoint'leri
│   └── ner_test.ipynb           # NER model test notebook'u
├── 📁 services/                  # Mikroservisler
│   ├── 📁 __pycache__/          # Python cache dosyaları
│   ├── geocoding_service_more.py # Gelişmiş coğrafi kodlama servisi
│   ├── geocoding_service.py     # Temel coğrafi kodlama servisi
│   ├── parsing_service.py       # NER tabanlı adres ayrıştırma
│   ├── postalcode_service.py    # Posta kodu servisi
│   └── preprocessing.py         # Metin ön işleme servisi
├── 📁 test/                     # Test dosyaları
│   ├── adres_skorlu.csv        # Skorlu test adresleri
│   ├── adres_veri.csv          # Test adres verileri
│   ├── best_score.py           # En iyi skor hesaplama
│   └── semantic_test.py        # Semantik benzerlik testleri
├── 📁 venv/                    # Python sanal ortamı
│   ├── 📁 etc/
│   │   └── 📁 jupyter/
│   ├── 📁 Include/
│   ├── 📁 Lib/
│   ├── 📁 Scripts/
│   ├── 📁 share/
│   └── pyvenv.cfg
├── .gitignore                  # Git ignore dosyası
├── benzerlik_test.py          # Benzerlik testi (2 uyarı)
├── enrichment_service.py      # Veri zenginleştirme servisi
├── hibrit_benzerlik_test.py   # Hibrit benzerlik testi (2 uyarı)  
├── matching_service.py        # Eşleştirme servisi
├── requirements.txt           # Python bağımlılıkları
├── semantic.py               # Semantik analiz servisi
├── test_preprocessing.py     # Ön işleme testleri
└── README.md                # Bu dosya

```

## 🔧 Teknoloji Stack'i

### Ana Framework ve Kütüphaneler
- **FastAPI**: RESTful API servisi
- **Streamlit**: İnteraktif web arayüzü
- **Transformers (Hugging Face)**: NER modelleri için
- **OSMnx**: OpenStreetMap veri çekimi
- **GeoPandas**: Coğrafi veri işleme

### NER Modelleri
- `savasy/bert-base-turkish-ner-cased`: Türkçe NER modeli
- `akdeniz27/mDeBERTa-v3-base-turkish-ner`: Gelişmiş Türkçe NER

### Benzerlik ve Eşleştirme
- **thefuzz**: Fuzzy string matching
- **sentence-transformers**: Semantik benzerlik
- **jellyfish**: String distance algoritmaları

### Coğrafi Servisler
- **Geoapify API**: Geocoding servisi
- **turkiye-api**: Türkiye posta kodu veritabanı
- **Redis**: API önbelleği (opsiyonel)

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8+
- Git
- İnternet bağlantısı (model indirme için)

### 1. Proje Klonlama
```bash
git clone https://github.com/PusulaAI77/AdressMatchingDemo.git 
cd AdressMatchingDemo
```

### 2. Sanal Ortam Oluşturma
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 4. Referans Veritabanı Oluşturma
```bash
python scripts/build_reference_db.py
```

### 5. API Servisini Başlatma
```bash
uvicorn api.main:app --reload --port 8000
```

### 6. Web Arayüzünü Çalıştırma
```bash
streamlit run app.py
```

## 📡 API Endpoint'leri

### 1. Sistem Durumu
```http
GET /status
```
**Yanıt:**
```json
{
    "status": "API çalışıyor",
    "version": "1.0.0",
    "timestamp": "2024-08-14T10:30:00Z"
}
```

### 2. Adres Ayrıştırma
```http
POST /parse
```
**İstek:**
```json
{
    "address": "Atatürk mah. 1234 sk. no:56 Çankaya/Ankara"
}
```
**Yanıt:**
```json
{
    "parsed_components": {
        "mahalle": "Atatürk Mahallesi",
        "sokak": "1234. Sokak",
        "numara": "56",
        "ilce": "Çankaya",
        "il": "Ankara"
    },
    "confidence_score": 0.89
}
```

### 3. Akıllı Eşleştirme
```http
POST /match
```
**İstek:**
```json
{
    "input_address": "Atatürk mah.",
    "candidates": [
        "Atatürk Mahallesi",
        "Ataturk Mahallesi",
        "Mustafa Kemal Mahallesi"
    ]
}
```
**Yanıt:**
```json
{
    "best_match": "Atatürk Mahallesi",
    "confidence_score": 0.95,
    "all_scores": [
        {"candidate": "Atatürk Mahallesi", "score": 0.95},
        {"candidate": "Ataturk Mahallesi", "score": 0.82},
        {"candidate": "Mustafa Kemal Mahallesi", "score": 0.45}
    ]
}
```

### 4. Ana Adres Çözümleme (End-to-End)
```http
POST /resolve_address
```
**İstek:**
```json
{
    "raw_address": "ataturk mh 1234 sk no 56 cankaya ankara"
}
```
**Yanıt:**
```json
{
    "input_address": "ataturk mh 1234 sk no 56 cankaya ankara",
    "standardized_address": "Atatürk Mahallesi 1234. Sokak No:56 Çankaya/Ankara",
    "components": {
        "mahalle": "Atatürk Mahallesi",
        "sokak": "1234. Sokak",
        "numara": "56",
        "ilce": "Çankaya",
        "il": "Ankara"
    },
    "geocoding": {
        "latitude": 39.9208,
        "longitude": 32.8541,
        "postal_code": "06420",
        "confidence": "high"
    },
    "processing_time_ms": 234,
    "overall_confidence": 0.91
}
```

### 5. Coğrafi Kodlama
```http
POST /geocode
```
**İstek:**
```json
{
    "address": "Atatürk Mahallesi 1234. Sokak No:56 Çankaya/Ankara"
}
```
**Yanıt:**
```json
{
    "latitude": 39.9208,
    "longitude": 32.8541,
    "postal_code": "06420",
    "formatted_address": "Atatürk Mah. 1234. Sk. No:56, 06420 Çankaya/Ankara",
    "confidence": "high"
}
```
🔬 Mevcut Servisler ve Testler

 🔧 Ana Servisler
| Dosya Adı                   | Açıklama                                                        |
| --------------------------- | --------------------------------------------------------------- |
| `parsing_service.py`        | NER (Named Entity Recognition) tabanlı adres ayrıştırma servisi |
| `matching_service.py`       | Akıllı adres eşleştirme algoritmaları                           |
| `geocoding_service.py`      | Temel coğrafi kodlama servisi (geocoding)                       |
| `geocoding_service_more.py` | Gelişmiş coğrafi kodlama özellikleri                            |
| `postalcode_service.py`     | Türkiye posta kodu sorgulama servisi                            |
| `enrichment_service.py`     | Adres verisini zenginleştirme servisi                           |
| `semantic.py`               | Semantik benzerlik analizi servisleri                           |


🧪 Test ve Geliştirme Dosyaları

| Dosya Adı                  | Açıklama                                  |
| -------------------------- | ----------------------------------------- |
| `test/adres_skorlu.csv`    | Skorlanmış örnek test adres verileri      |
| `test/adres_veri.csv`      | Ham test adres koleksiyonu                |
| `benzerlik_test.py`        | String benzerlik algoritmalarının testi   |
| `hibrit_benzerlik_test.py` | Hibrit skor bazlı eşleştirme testi        |
| `semantic_test.py`         | Semantik benzerlik algoritmalarının testi |
| `test_preprocessing.py`    | Metin ön işleme test dosyası              |
| `notebooks/ner_test.ipynb` | NER model performans analizi notebook’u   |

## 🎨 Web Arayüzü Özellikleri

- **Adres Girişi**: Kullanıcı dostu metin kutusu
- **Real-time İşleme**: Anında adres çözümleme
- **İnteraktif Harita**: Folium ile koordinat gösterimi
- **Detaylı Sonuçlar**: Ayrıştırılmış bileşenler ve güven skorları
- **Karşılaştırma**: Ham vs işlenmiş adres görünümü

## 🧪 Test Etme

### Unit Testleri Çalıştırma
```bash
python -m pytest tests/ -v
```

### Manuel Test Örnekleri
```bash
# API testi
curl -X POST "http://localhost:8000/resolve_address" \
     -H "Content-Type: application/json" \
     -d '{"raw_address": "bagdat cd. no 123 kadikoy istanbul"}'
```

## 📊 Performans ve Metrikler

- **Ayrıştırma Doğruluğu**: %89+ (test verisi üzerinde)
- **Eşleştirme Hassasiyeti**: %92+ (fuzzy + semantic)
- **API Yanıt Süresi**: <300ms (ortalama)
- **Coğrafi Doğrulama**: %96+ doğru koordinat

## 🛠️ Geliştirme ve Katkıda Bulunma

### Kod Standartları
- PEP 8 Python style guide
- Type hints kullanımı
- Docstring'ler için Google style
- Unit test coverage >80%

### Yeni Özellik Ekleme
1. Feature branch oluşturun: `git checkout -b feature/yeni-ozellik`
2. Kodunuzu yazın ve test edin
3. Pull request açın

## 🚨 Bilinen Sınırlamalar

- Çok kısa adresler (<3 kelime) için düşük performans
- Eski mahalle isimleri için sınırlı eşleştirme
- API rate limit: 1000 istek/saat (ücretsiz tier)
- Sadece Türkiye adresleri desteklenmektedir

## 📝 Gelecek Geliştirmeler

- [ ] Derin öğrenme tabanlı adres normalizasyonu
- [ ] Çoklu dil desteği
- [ ] Batch işleme API'si
- [ ] MongoDB entegrasyonu
- [ ] Docker containerization
- [ ] Kubernetes deployment

## 👥 Takım

- **Backend Developer**: API ve mikroservis mimarisi
- **ML Engineer**: NER modelleri ve eşleştirme algoritmaları
- **Frontend Developer**: Streamlit arayüzü ve UX
- **DevOps**: Deployment ve sistem yönetimi



## 🙏 Teşekkürler

- TEKNOFEST organizasyonu
- Hugging Face model sağlayıcıları
- OpenStreetMap topluluğu
