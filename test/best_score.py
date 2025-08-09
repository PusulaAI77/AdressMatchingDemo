import pandas as pd
from rapidfuzz import fuzz
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

# 1. CSV dosyasını oku
df = pd.read_csv("adres_veri.csv")

# 2. Benzerlik skorlarını hesapla (0-100 arasında)
df["skor"] = df.apply(lambda x: fuzz.token_sort_ratio(str(x["orijinal_adresler"]), str(x["eşleşecek_adresler"])) / 100, axis=1)

# 3. Threshold aralığını belirle
thresholds = np.arange(0.0, 1.01, 0.01)

best_threshold = 0
best_f1 = 0

# 4. Her threshold için performansı ölç
for t in thresholds:
    preds = (df["skor"] >= t).astype(int)
    f1 = f1_score(df["etiket"], preds)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = t

print(f"En iyi threshold: {best_threshold:.2f} | F1-Score: {best_f1:.4f}")

# 5. Sonuçları kaydet
df["tahmin"] = (df["skor"] >= best_threshold).astype(int)
df.to_csv("adres_skorlu.csv", index=False)

print("adres_skorlu.csv dosyası oluşturuldu.")
