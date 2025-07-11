#!/usr/bin/env python3

import pandas as pd

print("📋 Veri yapısı kontrol ediliyor...")

try:
    # Check emission dataset
    print("\n📊 emission_dataset.xlsx:")
    emission_df = pd.read_excel('data/emission_dataset.xlsx')
    print(f"Satır sayısı: {len(emission_df)}")
    print(f"Sütunlar: {list(emission_df.columns)}")
    print(f"İlk 3 satır:")
    print(emission_df.head(3))
    
except Exception as e:
    print(f"❌ emission_dataset.xlsx hatası: {e}")

try:
    # Check brands.xlsx
    print("\n🏭 brands.xlsx:")
    brands_df = pd.read_excel('brands.xlsx')
    print(f"Satır sayısı: {len(brands_df)}")
    print(f"Sütunlar: {list(brands_df.columns)}")
    print(f"İlk 3 satır:")
    print(brands_df.head(3))
    
except Exception as e:
    print(f"❌ brands.xlsx hatası: {e}")

try:
    # Check main emission file
    print("\n📈 Marka_Model_Emisyon Bilgisi_2021_2024.xls:")
    main_df = pd.read_excel('Marka_Model_Emisyon Bilgisi_2021_2024.xls')
    print(f"Satır sayısı: {len(main_df)}")
    print(f"Sütunlar: {list(main_df.columns)}")
    print(f"İlk 3 satır:")
    print(main_df.head(3))
    
except Exception as e:
    print(f"❌ Ana emisyon dosyası hatası: {e}")

try:
    # Check brands_models_generations.xlsx
    print("\n🔧 brands_models_generations.xlsx:")
    bmg_df = pd.read_excel('brands_models_generations.xlsx')
    print(f"Satır sayısı: {len(bmg_df)}")
    print(f"Sütunlar: {list(bmg_df.columns)}")
    print(f"İlk 3 satır:")
    print(bmg_df.head(3))
    
except Exception as e:
    print(f"❌ brands_models_generations.xlsx hatası: {e}")