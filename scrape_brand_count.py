import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.auto-data.net/tr/allbrands"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Marka kutularını bul (her bir marka genellikle bir a etiketi içinde)
brand_boxes = soup.find_all('a', class_='marki_blok')

brand_names = [brand.get_text(strip=True) for brand in brand_boxes]

print(f"Tıklanabilir marka sayısı: {len(brand_names)}")

# Excel dosyasına kaydet
brands_df = pd.DataFrame(brand_names, columns=["Marka Adı"])
brands_df.to_excel("brands.xlsx", index=False)
print("brands.xlsx dosyasına kaydedildi.") 