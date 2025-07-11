import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_hyundai_data():
    # URL'yi tanımla
    url = "https://www.auto-data.net/tr/hyundai-accent-v-hatchback-1.6-smartstream-dpi-120hp-cvt-43661"
    
    # Daha gerçekçi headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    # Rastgele bekleme süresi ekle
    time.sleep(random.uniform(1, 3))
    
    try:
        # Sayfayı çek
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        
        # HTML'i parse et
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tüm tabloları bul
        tables = soup.find_all('table')
        
        # Verileri saklamak için liste
        all_data = []
        found_general_info = False
        
        # Her tablo için
        for table in tables:
            # Tablonun ilk satırını kontrol et
            first_row = table.find('tr')
            if first_row and 'Genel bilgi' in first_row.get_text():
                found_general_info = True
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if cols:
                        row_data = [col.get_text(strip=True) for col in cols]
                        if any(row_data):  # Boş satırları atla
                            all_data.append(row_data)
                break  # Genel bilgi tablosunu bulduktan sonra döngüden çık
        
        if not found_general_info:
            print("Uyarı: Genel bilgi tablosu bulunamadı!")
            return
            
        if not all_data:
            print("Uyarı: Tablolardan veri çekilemedi!")
            return
        
        # DataFrame oluştur
        df = pd.DataFrame(all_data)
        
        # İlk satırı sütun isimleri olarak kullan ve kaldır
        df.columns = ['Özellik', 'Değer']
        
        # Excel dosyasına kaydet
        df.to_excel('hyundai_accent_genel_bilgi.xlsx', index=False)
        print("Genel bilgi verileri başarıyla 'hyundai_accent_genel_bilgi.xlsx' dosyasına kaydedildi.")
        
        # Verileri ekrana yazdır
        print("\nÇekilen veriler:")
        print(df.to_string())
        
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    scrape_hyundai_data() 