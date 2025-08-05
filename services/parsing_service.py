# services/parsing_service.py

from transformers import pipeline
from services.preprocessing import temizle
from fastapi.encoders import jsonable_encoder

# NER pipeline oluştur
ner_model = pipeline(
    task="ner",
    model="savasy/bert-base-turkish-ner-cased",
    tokenizer="savasy/bert-base-turkish-ner-cased",
    grouped_entities=True
)



def parse_address(address: str):
    temiz_adres = temizle(address)
    sonuc_raw = ner_model(temiz_adres)

    # Burada her bir entity'yi JSON uyumlu hale getiriyoruz
    sonuc = []
    for ent in sonuc_raw:
        sonuc.append({
            "word": ent.get("word"),
            "entity_group": ent.get("entity_group"),
            "score": float(ent.get("score", 0)),  # float32 yerine float
            "start": ent.get("start"),
            "end": ent.get("end")
        })

    return {
        "temiz_adres": temiz_adres,
        "entities": sonuc  # Artık jsonable_encoder'a gerek yok
    }

