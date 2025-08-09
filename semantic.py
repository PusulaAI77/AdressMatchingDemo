from sentence_transformers import SentenceTransformer, util     # önceden eğitilmiş BERT tabanlı modeller
import torch                                                    # Modeli GPU’da çalıştırmak için.
from services.preprocessing import temizle  

device = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "dbmdz/bert-base-turkish-cased"   

model = SentenceTransformer(MODEL_NAME, device=device)

# Burada önce iki metin (adres) temizleniyor.

def semantic_similarity(a: str, b: str) -> float:
    a_proc = temizle(a) if 'temizle' in globals() else a.lower()
    b_proc = temizle(b) if 'temizle' in globals() else b.lower()

# İki adres, model aracılığıyla vektörlere (sayısal temsillere) dönüştürülüyor.

    emb = model.encode([a_proc, b_proc], convert_to_tensor=True, normalize_embeddings=True)
    cos = util.cos_sim(emb[0], emb[1]).item()   # -1..1
    return float(cos)

# Test
# print(semantic_similarity("TBMM Binası", "Türkiye Büyük Millet Meclisi"))
