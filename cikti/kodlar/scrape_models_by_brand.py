import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

# Marka adını normalize eden fonksiyon
def normalize(text):
    if not isinstance(text, str):
        return ''
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower().replace('-', ' ').replace('–', ' ').replace('  ', ' ').strip()

# Manuel marka eşleme tablosu (gerekirse genişletilebilir)
manual_map = {
    'vw porsche': ['porsche', 'vw porsche'],
    'mercedes benz': ['mercedes benz', 'mercedes-benz'],
    'ds': ['ds', 'ds automobiles'],
    # Gerekirse diğer eşleşmeler eklenebilir
}

def get_all_possible_names(brand):
    names = [brand]
    for k, v in manual_map.items():
        if brand == k:
            names.extend(v)
    return list(set(names))

# Eksik olan markalar
not_in_brands = [
    'KARSAN',
    'SKYWELL',
    'KG MOBILITY – SSANGYONG',
    'NETA',
    'FARIZON',
    'OTOKAR'
]

# brands.xlsx dosyasını oku
brands_df = pd.read_excel('brands.xlsx')
brands_list = [normalize(x) for x in brands_df['Marka Adı']]

# emission_dataset.xlsx dosyasındaki perakende sayfasını oku
perakende_df = pd.read_excel('data/emission_dataset.xlsx', sheet_name='perakende')
perakende_brands = [normalize(x) for x in perakende_df['Marka'].unique()]

# Tüm uygun markalar (eksik olmayanlar)
common_brands = [brand for brand in perakende_brands if normalize(brand) not in [normalize(x) for x in not_in_brands] and brand in brands_list]
print('common_brands:', common_brands)

# Ana sayfadan marka linklerini çek
url = "https://www.auto-data.net/tr/allbrands"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Sitedeki tüm marka adlarını ve linklerini topla
site_brand_links = {}
for a in soup.find_all('a', class_='marki_blok'):
    name = normalize(a.get_text(strip=True))
    href = a.get('href')
    if name and href:
        if name not in site_brand_links:
            site_brand_links[name] = []
        site_brand_links[name].append('https://www.auto-data.net' + href)

# Her common_brand için, eşleşen tüm site linklerini bul
brand_links = {}
for brand in common_brands:
    possible_names = get_all_possible_names(brand)
    found_links = []
    for pname in possible_names:
        for sitename, links in site_brand_links.items():
            if pname == sitename or pname in sitename or sitename in pname:
                found_links.extend(links)
    if found_links:
        brand_links[brand] = list(set(found_links))

print('Eşleşen marka linkleri:', brand_links)

all_generations = []
for brand, links in brand_links.items():
    for link in links:
        print(f"{brand} markası işleniyor: {link}")
        time.sleep(2)
        try:
            r = requests.get(link, headers=headers, timeout=15)
            if r.status_code != 200:
                print(f"{brand} için sayfa yüklenemedi! Kod: {r.status_code}")
                continue
            s = BeautifulSoup(r.content, 'html.parser')
            model_blocks = s.find_all('a', class_='modeli')
            print(f"{brand} için bulunan model sayısı: {len(model_blocks)}")
            for m in model_blocks:
                model_name = m.get_text(strip=True)
                model_url = m.get('href')
                if model_url:
                    model_url = 'https://www.auto-data.net' + model_url
                    # Şimdi modelin altındaki nesilleri/versiyonları çek
                    try:
                        time.sleep(1)
                        r2 = requests.get(model_url, headers=headers, timeout=15)
                        if r2.status_code != 200:
                            print(f"{brand} - {model_name} için model sayfası yüklenemedi! Kod: {r2.status_code}")
                            continue
                        s2 = BeautifulSoup(r2.content, 'html.parser')
                        # Tüm <tr> satırlarını bul
                        gen_rows = s2.find_all('tr')
                        found_generation = False
                        found_names = []
                        for row in gen_rows:
                            gen_name_tag = row.find('strong', class_='tit')
                            if not gen_name_tag:
                                gen_name_tag = row.find('span', class_='tit')
                            if gen_name_tag:
                                gen_name = gen_name_tag.get_text(strip=True)
                                found_names.append(gen_name)
                                gen_url_tag = row.find('a', href=True)
                                gen_url = gen_url_tag.get('href') if gen_url_tag else ''
                                if gen_url:
                                    gen_url = 'https://www.auto-data.net' + gen_url
                                all_generations.append({
                                    'Marka': brand,
                                    'Model': model_name,
                                    'Model_URL': model_url,
                                    'Nesil/Versiyon': gen_name,
                                    'Nesil_URL': gen_url,
                                    'Alt_Versiyon': '',
                                    'Alt_Versiyon_URL': ''
                                })
                                found_generation = True
                        print(f"{brand} - {model_name} için bulunan nesil/versiyon sayısı: {len(found_names)}")
                        if found_names:
                            print(f"Bulunan nesil/versiyon isimleri: {found_names}")
                        # Her nesil/versiyonun alt versiyonlarını çek
                        for row in gen_rows:
                            gen_name_tag = row.find('strong', class_='tit')
                            if not gen_name_tag:
                                gen_name_tag = row.find('span', class_='tit')
                            if gen_name_tag:
                                gen_name = gen_name_tag.get_text(strip=True)
                                gen_url_tag = row.find('a', href=True)
                                gen_url = gen_url_tag.get('href') if gen_url_tag else ''
                                if gen_url:
                                    gen_url = 'https://www.auto-data.net' + gen_url
                                    print(f"    Nesil: {gen_name}")
                                    # Alt versiyonları çek
                                    try:
                                        time.sleep(0.5)
                                        r3 = requests.get(gen_url, headers=headers, timeout=10)
                                        if r3.status_code == 200:
                                            s3 = BeautifulSoup(r3.content, 'html.parser')
                                            alt_rows = s3.find_all('tr')
                                            for alt_row in alt_rows:
                                                alt_name_tag = alt_row.find('span', class_='tit')
                                                if alt_name_tag:
                                                    alt_name = alt_name_tag.get_text(strip=True)
                                                    alt_url_tag = alt_row.find('a', href=True)
                                                    alt_url = alt_url_tag.get('href') if alt_url_tag else ''
                                                    if alt_url:
                                                        alt_url = 'https://www.auto-data.net' + alt_url
                                                    print(f"      Alt Versiyon: {alt_name}")
                                                    all_generations.append({
                                                        'Marka': brand,
                                                        'Model': model_name,
                                                        'Model_URL': model_url,
                                                        'Nesil/Versiyon': gen_name,
                                                        'Nesil_URL': gen_url,
                                                        'Alt_Versiyon': alt_name,
                                                        'Alt_Versiyon_URL': alt_url
                                                    })
                                    except Exception as e:
                                        print(f"      Alt versiyonlar çekilemedi: {e}")
                        # Eğer hiç nesil/versiyon yoksa, modelin kendisini ekle
                        if not found_generation:
                            all_generations.append({
                                'Marka': brand,
                                'Model': model_name,
                                'Model_URL': model_url,
                                'Nesil/Versiyon': '',
                                'Nesil_URL': '',
                                'Alt_Versiyon': '',
                                'Alt_Versiyon_URL': ''
                            })
                    except Exception as e:
                        print(f"{brand} - {model_name} için hata oluştu: {e}")
        except Exception as e:
            print(f"{brand} için hata oluştu: {e}")

models_df = pd.DataFrame(all_generations)
# Alt_Versiyon sütununda boş olan satırları sil
models_df = models_df[models_df['Alt_Versiyon'].notna() & (models_df['Alt_Versiyon'] != '')]
models_df.to_excel('brands_models_generations.xlsx', index=False)
print('Tüm uygun markaların model, nesil/versiyon ve alt versiyon listeleri brands_models_generations.xlsx dosyasına kaydedildi.')