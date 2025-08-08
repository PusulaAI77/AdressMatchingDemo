
import os                               #klasör ve dosya işlemleri için.
import osmnx as ox                      #harita verilerini OpenStreetMap’ten almak için.
import geopandas as gpd                 #coğrafi (harita) verileri işlemek için.
import pandas as pd                     #normal veri işlemleri için.
from sqlalchemy import create_engine    #veritabanı bağlantısı kurmak için

# Şehir listesi
sehirler = ["Istanbul, Turkey", "Ankara, Turkey", "Izmir, Turkey", "Bursa, Turkey", "Antalya, Turkey"]

# Çıktı klasörlerini oluştur
os.makedirs("csv", exist_ok=True)
os.makedirs("sqlite", exist_ok=True)

# SQLite veritabanı bağlantısı
engine = None  # Veritabanı bağlantısı yok, sadece CSV kullanacağız


def temizle_sokak_ismi(name):
    if isinstance(name, str):
        return name.lower().strip()
    return None

def veri_topla(sehir):
    print(f"[+] Veri çekiliyor: {sehir}")
    
    try:
        # Sokak ağı verisini al
        G = ox.graph_from_place(sehir, network_type='drive')
        edges = ox.graph_to_gdfs(G, nodes=False)
        
        # Sadece isimli sokakları filtrele
        sokaklar = edges[edges['name'].notnull()].copy()
        sokaklar['name_clean'] = sokaklar['name'].apply(temizle_sokak_ismi)
        sokaklar = sokaklar[['name_clean', 'geometry']]
        sokaklar.drop_duplicates(inplace=True)

        # CSV'ye kaydet
        csv_path = f"csv/{sehir.split(',')[0].lower()}_sokaklar.csv"
        sokaklar.to_csv(csv_path, index=False)
        print(f"    ↪ Sokaklar CSV'ye kaydedildi: {csv_path}")

    except Exception as e:
        print(f"    ↪ Sokak verisi çekme hatası: {e}")

    try:
        # İlçe/mahalle geometrileri - DÜZELTME: ox.features.geometries_from_place yerine ox.geometries_from_place
        geo = ox.geometries_from_place(sehir, tags={'admin_level': ['8', '9']})
        
        if not geo.empty:
            # geometry sütunu zaten mevcut, diğer sütunları kontrol et
            if 'name' in geo.columns:
                geo = geo.reset_index()
                geo['name_clean'] = geo['name'].apply(temizle_sokak_ismi)
                geo = geo[['name_clean', 'geometry']]
            else:
                # name sütunu yoksa sadece geometry kullan
                geo = geo.reset_index()
                geo = geo[['geometry']]
            
            geo.dropna(subset=['geometry'], inplace=True)

            # CSV'ye kaydet
            csv_path = f"csv/{sehir.split(',')[0].lower()}_ilce_mahalle.csv"
            geo.to_csv(csv_path, index=False)
            print(f"    ↪ İlçe/mahalle verileri kaydedildi: {csv_path}")
        else:
            print("    ↪ İlçe/mahalle verisi bulunamadı.")
            
    except Exception as e:
        print(f"    ↪ İlçe/mahalle verisi çekme hatası: {e}")

# Tüm şehirler için veri çek
for sehir in sehirler:
    try:
        veri_topla(sehir)
        print(f"    ✅ {sehir} tamamlandı\n")
    except Exception as e:
        print(f"[!] Genel hata oluştu: {sehir} - {e}\n")

print("✅ Tüm veriler işleme tamamlandı.")