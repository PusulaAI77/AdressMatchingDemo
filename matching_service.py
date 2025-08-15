# services/matching_service.py
 
import pandas as pd
from services.preprocessing import temizle
from semantic import semantic_similarity
from hibrit_benzerlik_test import adres_benzerlik
import os
import glob
 
DATA_FOLDER = "data"  # data klasörü
 
def load_data():
    all_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
    df_list = []
    for f in all_files:
        df = pd.read_csv(f, usecols=["name_clean"])  # sadece name_clean sütunu okunuyor
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df
 
adres_db = load_data()
 
def hesapla_güven_skoru(fuzzy, semantic, w_fuzzy=0.5, w_semantic=0.5):
    return w_fuzzy * fuzzy + w_semantic * semantic
 
def match_address(input_address):
    input_addr_clean = temizle(input_address)
 
    en_iyi_skor = -1
    en_iyi_adres = None
    en_iyi_fuzzy = 0
    en_iyi_semantic = 0
 
    for idx, row in adres_db.iterrows():
        aday_adres = row["name_clean"]
        aday_adres_clean = temizle(aday_adres)
 
        fuzzy = adres_benzerlik(input_addr_clean, aday_adres_clean)
        semantic = semantic_similarity(input_addr_clean, aday_adres_clean) * 100  # %100'e ölçekle
 
        final = hesapla_güven_skoru(fuzzy, semantic)
 
        if final > en_iyi_skor:
            en_iyi_skor = final
            en_iyi_adres = aday_adres
            en_iyi_fuzzy = fuzzy
            en_iyi_semantic = semantic
 
    return {
        "matched_address": en_iyi_adres,
        "fuzzy_score": en_iyi_fuzzy,
        "semantic_score": en_iyi_semantic,
        "final_score": round(en_iyi_skor, 2)
    }

