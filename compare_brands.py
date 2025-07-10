import pandas as pd

# brands.xlsx dosyasını oku
brands_df = pd.read_excel('brands.xlsx')
brands_list = brands_df['Marka Adı'].str.upper().str.strip().tolist()

# emission_dataset.xlsx dosyasındaki perakende sayfasını oku
perakende_df = pd.read_excel('data/emission_dataset.xlsx', sheet_name='perakende')
perakende_brands = perakende_df['Marka'].str.upper().str.strip().unique().tolist()

# Perakende sayfasında olup brands.xlsx'te olmayan markaları bul
not_in_brands = [brand for brand in perakende_brands if brand not in brands_list]

if not_in_brands:
    print("Perakende sayfasında olup brands.xlsx dosyasında olmayan markalar:")
    for marka in not_in_brands:
        print(marka)
else:
    print("Tüm perakende markaları brands.xlsx dosyasında mevcut.") 