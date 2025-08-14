import streamlit as st
import requests
import json
import folium
from streamlit_folium import folium_static
import re

st.set_page_config(page_title="Adres Çözümleme Demo", page_icon="🗺️")

st.title("🗺️ TEKNOFEST Adres Çözümleme Sistemi")

# API URL
API_URL = "http://localhost:8000"

# Adres girişi
address_input = st.text_area("Adres Girin:", placeholder="Örn: ataturk mh 1234 sk no 56 cankaya ankara")

if st.button("🔍 Adresi Çözümle"):
    if address_input:
        try:
            # API isteği
            response = requests.post(
                f"{API_URL}/resolve_address",
                json={"address": address_input}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Sonuçları göster
                st.success("✅ Adres başarıyla çözümlendi!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📝 Ham vs İşlenmiş")
                    st.write("**Girilen Adres:**", result['input_address'])
                    
                    if 'parsed' in result:
                        st.write("**Ayrıştırılmış:**", result['parsed'])
                
                with col2:
                    st.subheader("🎯 Eşleştirme & Zenginleştirme")
                    
                    if 'matched' in result:
                        st.write("**Eşleşme:**", result['matched'])
                    
                    if 'enriched' in result:
                        st.write("**Zenginleştirilmiş:**", result['enriched'])

                # BONUS: İnteraktif Harita Gösterimi
                st.subheader("🗺️ İnteraktif Harita Görünümü")
                
                # Koordinat çıkarma fonksiyonu
                def extract_coordinates(data):
                    """API sonucundan koordinatları çıkarır"""
                    coordinates = []
                    
                    # JSON stringini recursive olarak tara
                    def search_coords(obj, path=""):
                        if isinstance(obj, dict):
                            for key, value in obj.items():
                                new_path = f"{path}.{key}" if path else key
                                
                                # Koordinat anahtar kelimelerini ara
                                if key.lower() in ['latitude', 'lat', 'enlem'] and value is not None:
                                    try:
                                        lat = float(value)
                                        # Longitude'u da ara
                                        lon_keys = ['longitude', 'lon', 'lng', 'boylam']
                                        for lon_key in lon_keys:
                                            if lon_key in obj and obj[lon_key] is not None:
                                                lon = float(obj[lon_key])
                                                coordinates.append((lat, lon))
                                                break
                                    except (ValueError, TypeError):
                                        pass
                                
                                # Koordinat çiftlerini ara
                                elif key.lower() in ['coordinates', 'coord', 'location'] and value is not None:
                                    if isinstance(value, list) and len(value) == 2:
                                        try:
                                            if value[0] is not None and value[1] is not None:
                                                lat, lon = float(value[0]), float(value[1])
                                                coordinates.append((lat, lon))
                                        except (ValueError, TypeError):
                                            try:
                                                if value[0] is not None and value[1] is not None:
                                                    lon, lat = float(value[0]), float(value[1])
                                                    coordinates.append((lat, lon))
                                            except (ValueError, TypeError):
                                                pass
                                
                                search_coords(value, new_path)
                        
                        elif isinstance(obj, list):
                            for i, item in enumerate(obj):
                                search_coords(item, f"{path}[{i}]")
                        
                        elif isinstance(obj, str):
                            # String içinde koordinat pattern'i ara
                            coord_patterns = [
                                r'(\d+\.\d+),\s*(\d+\.\d+)',  # "39.925, 32.837"
                                r'lat:\s*(\d+\.\d+).*lon:\s*(\d+\.\d+)',  # "lat: 39.925, lon: 32.837"
                                r'(\d+\.\d+)\s+(\d+\.\d+)'   # "39.925 32.837"
                            ]
                            
                            for pattern in coord_patterns:
                                matches = re.findall(pattern, obj)
                                for match in matches:
                                    try:
                                        lat, lon = float(match[0]), float(match[1])
                                        # Türkiye sınırları kontrolü
                                        if 36.0 <= lat <= 42.0 and 26.0 <= lon <= 45.0:
                                            coordinates.append((lat, lon))
                                    except:
                                        pass
                    
                    search_coords(data)
                    return coordinates

                # Koordinatları çıkar
                coords = extract_coordinates(result)
                
                if coords:
                    # İlk koordinatı kullan
                    lat, lon = coords[0]
                    
                    # Folium haritası oluştur
                    m = folium.Map(
                        location=[lat, lon],
                        zoom_start=15,
                        tiles='OpenStreetMap'
                    )
                    
                    # İşaretçi ekle
                    folium.Marker(
                        [lat, lon],
                        popup=f"""
                        <div style="width: 200px;">
                            <b>📍 Çözümlenen Adres</b><br>
                            <i>{result['input_address']}</i><br><br>
                            <b>Koordinatlar:</b><br>
                            Enlem: {lat}<br>
                            Boylam: {lon}
                        </div>
                        """,
                        tooltip="Adres Konumu",
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(m)
                    
                    # Haritayı Streamlit'te göster
                    folium_static(m, width=700, height=500)
                    
                    # Koordinat bilgisi
                    st.info(f"📍 **Konum:** {lat:.6f}, {lon:.6f}")
                    
                    # Çoklu koordinat varsa uyarı
                    if len(coords) > 1:
                        st.warning(f"ℹ️ Toplam {len(coords)} koordinat bulundu. İlki haritada gösterildi.")
                        
                        with st.expander("🔍 Bulunan Tüm Koordinatlar"):
                            for i, (lat_i, lon_i) in enumerate(coords):
                                st.write(f"**{i+1}.** {lat_i:.6f}, {lon_i:.6f}")

                else:
                    st.warning("🔍 API sonucunda koordinat bulunamadı.")
                    st.info("💡 İpucu: Enrichment servisinin koordinat döndürdüğünden emin olun.")
                    
                    # Varsayılan Türkiye haritası göster
                    default_map = folium.Map(
                        location=[39.9334, 32.8597],  # Ankara
                        zoom_start=6,
                        tiles='OpenStreetMap'
                    )
                    
                    folium.Marker(
                        [39.9334, 32.8597],
                        popup="Varsayılan Konum: Ankara",
                        tooltip="Koordinat bulunamadı",
                        icon=folium.Icon(color='blue', icon='question-sign')
                    ).add_to(default_map)
                    
                    folium_static(default_map, width=700, height=400)

                # JSON çıktısı
                with st.expander("📋 Detaylı JSON Çıktısı"):
                    st.json(result)
                
            else:
                st.error(f"❌ API Hatası: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
            st.info("💡 API servisinin çalıştığından emin olun")
    
    else:
        st.warning("⚠️ Lütfen bir adres girin!")

# Sidebar bilgi
with st.sidebar:
    st.header("ℹ️ Sistem Bilgisi")
    st.info("""
    **TEKNOFEST 2024**  
    Adres Çözümleme Sistemi
    
    🔧 **Teknolojiler:**
    - NER (Turkish BERT)
    - Hibrit Puanlama  
    - GIS Doğrulama
    - İnteraktif Haritalar
    """)
    
    st.header("🎯 Kullanım İpuçları")
    st.write("""
    1. Tam adres yazın
    2. İlçe/il bilgisi ekleyin  
    3. Sokak/mahalle belirtin
    4. Haritada sonucu görün
    """)