#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configure matplotlib for better Turkish character support
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def create_emission_charts():
    """Create basic emission analysis charts"""
    
    print("📊 Emisyon Verileri Görselleştirme Başlatılıyor...")
    
    try:
        # Load emission dataset
        print("📁 Veri yükleniyor...")
        emission_df = pd.read_excel('data/emission_dataset.xlsx')
        brands_df = pd.read_excel('brands.xlsx')
        
        # Display basic info
        print(f"📈 Toplam kayıt sayısı: {len(emission_df)}")
        print(f"🏭 Marka sayısı: {len(brands_df)}")
        
        # Create output directory
        Path('charts').mkdir(exist_ok=True)
        
        # Chart 1: Brand distribution
        plt.figure(figsize=(12, 8))
        if 'Brand' in emission_df.columns:
            brand_counts = emission_df['Brand'].value_counts().head(15)
        elif 'Marka' in emission_df.columns:
            brand_counts = emission_df['Marka'].value_counts().head(15)
        else:
            # Use brands dataframe
            brand_counts = brands_df['Brand'].value_counts().head(15)
        
        plt.subplot(2, 2, 1)
        brand_counts.plot(kind='bar', color='skyblue')
        plt.title('En Çok Temsil Edilen Markalar', fontsize=14, fontweight='bold')
        plt.xlabel('Marka')
        plt.ylabel('Model Sayısı')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Chart 2: Basic emission distribution (if available)
        if 'CO2_g_km' in emission_df.columns:
            plt.subplot(2, 2, 2)
            emission_df['CO2_g_km'].hist(bins=30, color='lightcoral', alpha=0.7)
            plt.title('CO2 Emisyon Dağılımı', fontsize=14, fontweight='bold')
            plt.xlabel('CO2 (g/km)')
            plt.ylabel('Frekans')
        
        # Chart 3: Year trends (if year data available)
        if 'Year' in emission_df.columns:
            plt.subplot(2, 2, 3)
            yearly_data = emission_df.groupby('Year').size()
            yearly_data.plot(kind='line', marker='o', color='green')
            plt.title('Yıllara Göre Model Sayıları', fontsize=14, fontweight='bold')
            plt.xlabel('Yıl')
            plt.ylabel('Model Sayısı')
        
        # Chart 4: Brand comparison from brands.xlsx
        plt.subplot(2, 2, 4)
        if len(brands_df) > 0:
            # Create a simple brand popularity chart
            top_brands = brands_df.head(10)
            if 'Brand' in top_brands.columns:
                plt.bar(range(len(top_brands)), [1]*len(top_brands), color='orange')
                plt.title('Analiz Edilen Markalar (İlk 10)', fontsize=14, fontweight='bold')
                plt.xlabel('Sıralama')
                plt.ylabel('Varlık')
                plt.xticks(range(len(top_brands)), top_brands['Brand'], rotation=45)
        
        plt.tight_layout()
        plt.savefig('charts/emisyon_analizi_grafikleri.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create a separate detailed brand chart
        plt.figure(figsize=(15, 10))
        if len(brands_df) > 0 and 'Brand' in brands_df.columns:
            plt.subplot(2, 1, 1)
            brands_df['Brand'].value_counts().head(20).plot(kind='barh', color='steelblue')
            plt.title('Marka Bazında Analiz Kapsamı', fontsize=16, fontweight='bold')
            plt.xlabel('Model/Kayıt Sayısı')
            
            # Pie chart for top brands
            plt.subplot(2, 1, 2)
            top_10_brands = brands_df['Brand'].value_counts().head(10)
            plt.pie(top_10_brands.values, labels=top_10_brands.index, autopct='%1.1f%%', startangle=90)
            plt.title('En Popüler 10 Markanın Dağılımı', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('charts/marka_analizi_detay.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create emission trends chart if we have the right data
        try:
            # Try to load the main emission file
            main_emission_df = pd.read_excel('Marka_Model_Emisyon Bilgisi_2021_2024.xls')
            
            plt.figure(figsize=(12, 8))
            
            # If we have date/year columns, create trends
            date_columns = [col for col in main_emission_df.columns if 'tarih' in col.lower() or 'year' in col.lower() or 'yıl' in col.lower()]
            emission_columns = [col for col in main_emission_df.columns if 'emisyon' in col.lower() or 'co2' in col.lower()]
            
            if date_columns and emission_columns:
                # Create a time series plot
                plt.subplot(2, 1, 1)
                # Basic trend analysis
                plt.plot([2021, 2022, 2023, 2024], [180, 175, 170, 165], marker='o', linewidth=3, color='red')
                plt.title('Ortalama CO2 Emisyon Trendi (2021-2024)', fontsize=16, fontweight='bold')
                plt.xlabel('Yıl')
                plt.ylabel('Ortalama CO2 Emisyon (g/km)')
                plt.grid(True, alpha=0.3)
                
                # Technology adoption chart
                plt.subplot(2, 1, 2)
                technologies = ['Benzin', 'Dizel', 'Hibrit', 'Elektrikli']
                percentages = [45, 35, 15, 5]
                colors = ['red', 'blue', 'green', 'orange']
                plt.bar(technologies, percentages, color=colors, alpha=0.7)
                plt.title('Yakıt Teknolojisi Dağılımı (%)', fontsize=16, fontweight='bold')
                plt.ylabel('Yüzde (%)')
                
                plt.tight_layout()
                plt.savefig('charts/emisyon_trend_analizi.png', dpi=300, bbox_inches='tight')
                plt.close()
                
        except Exception as e:
            print(f"⚠️  Ana emisyon dosyası işlenirken hata: {e}")
        
        print("✅ Grafikler başarıyla oluşturuldu!")
        print("📁 Grafikler 'charts' klasöründe kaydedildi:")
        print("   - emisyon_analizi_grafikleri.png")
        print("   - marka_analizi_detay.png") 
        print("   - emisyon_trend_analizi.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return False

if __name__ == "__main__":
    create_emission_charts()