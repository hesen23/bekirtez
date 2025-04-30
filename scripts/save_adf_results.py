import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import os

# Doğru dosya yolunu oluştur
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(os.path.dirname(current_dir), 'data', 'emission_dataset.xlsx')
results_path = os.path.join(os.path.dirname(current_dir), 'results', 'adf_test_results.xlsx')

# Excel dosyasını oku
df = pd.read_excel(excel_path, sheet_name='ek1')

# ADF testi fonksiyonu
def adf_test(series, title=''):
    """
    Augmented Dickey-Fuller testi uygular ve sonuçları döndürür
    """
    # ADF testini uygula
    result = adfuller(series.dropna())
    
    # Sonuçları sözlük olarak döndür
    return {
        'Seri': title,
        'ADF İstatistiği': result[0],
        'p-değeri': result[1],
        'Kritik Değer (%1)': result[4]['1%'],
        'Kritik Değer (%5)': result[4]['5%'],
        'Kritik Değer (%10)': result[4]['10%'],
        'Durağanlık Durumu': 'Durağan' if result[1] <= 0.05 else 'Durağan Değil'
    }

# Orijinal ve fark alınmış seri için testleri uygula
results = []
results.append(adf_test(df['ADET'], 'Orijinal Seri'))
results.append(adf_test(df['ADET'].diff().dropna(), 'Birinci Fark Alınmış Seri'))

# Sonuçları DataFrame'e dönüştür
results_df = pd.DataFrame(results)

# Excel'e kaydet
results_df.to_excel(results_path, index=False)
print(f"Sonuçlar {results_path} dosyasına kaydedildi.") 