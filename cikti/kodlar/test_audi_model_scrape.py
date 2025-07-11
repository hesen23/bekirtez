import requests
from bs4 import BeautifulSoup

url = 'https://www.auto-data.net/tr/audi-brand-41'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Tüm linkleri ve class'larını yazdır
for a in soup.find_all('a'):
    print(a.get('class'), a.get_text(strip=True), a.get('href'))

# Ayrıca model bloklarını bulmayı dene
model_blocks = soup.find_all('a', class_='modeli')
print(f"\nclass_='modeli' ile bulunan model sayısı: {len(model_blocks)}")
for m in model_blocks:
    print(m.get_text(strip=True), m.get('href')) 