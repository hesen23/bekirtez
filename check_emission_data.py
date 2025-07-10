import pandas as pd

def check_emission_data():
    # Excel dosyasını oku
    df = pd.read_excel('data/emission_dataset.xlsx', sheet_name=None)
    
    # Sayfa isimlerini yazdır
    print("Excel dosyasındaki sayfalar:")
    for sheet_name in df.keys():
        print(f"\n{sheet_name} sayfası:")
        print(df[sheet_name].columns.tolist())
        print("\nİlk 5 satır:")
        print(df[sheet_name].head())

if __name__ == "__main__":
    check_emission_data() 