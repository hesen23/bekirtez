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
    """Create emission analysis charts using correct column names"""
    
    print("📊 Emisyon Verileri Görselleştirme Başlatılıyor...")
    
    try:
        # Load datasets
        print("📁 Veri dosyaları yükleniyor...")
        
        # 1. Monthly sales data (emission_dataset.xlsx)
        emission_df = pd.read_excel('data/emission_dataset.xlsx')
        print(f"📈 Aylık satış verileri: {len(emission_df)} kayıt")
        
        # 2. Brands list (brands.xlsx)
        brands_df = pd.read_excel('brands.xlsx')
        print(f"🏭 Marka sayısı: {len(brands_df)}")
        
        # 3. Detailed brand-model data (brands_models_generations.xlsx)
        bmg_df = pd.read_excel('brands_models_generations.xlsx')
        print(f"🔧 Detaylı model verileri: {len(bmg_df)} kayıt")
        
        # Create output directory
        Path('charts').mkdir(exist_ok=True)
        
        # === CHART 1: Monthly Sales Trends (2021-2024) ===
        plt.figure(figsize=(15, 12))
        
        # Subplot 1: Yearly sales comparison
        plt.subplot(2, 2, 1)
        yearly_sales = emission_df.groupby('Yıl')['Adet'].sum()
        bars = plt.bar(yearly_sales.index, yearly_sales.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        plt.title('Yıllık Toplam Otomobil Satışları', fontsize=14, fontweight='bold')
        plt.xlabel('Yıl')
        plt.ylabel('Satış Adedi')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom', fontsize=10)
        
        # Subplot 2: Monthly trend over years
        plt.subplot(2, 2, 2)
        
        # Create a more detailed monthly analysis
        monthly_data = emission_df.copy()
        monthly_data['Yıl_Ay'] = monthly_data['Yıl'].astype(str) + '-' + monthly_data['Ay']
        
        # Plot line chart for monthly trends
        x_positions = range(len(monthly_data))
        plt.plot(x_positions, monthly_data['Adet'], marker='o', linewidth=2, markersize=4, color='#E74C3C')
        plt.title('Aylık Satış Trendi (2021-2024)', fontsize=14, fontweight='bold')
        plt.xlabel('Dönem')
        plt.ylabel('Satış Adedi')
        plt.xticks(range(0, len(monthly_data), 6), 
                  [monthly_data.iloc[i]['Yıl_Ay'] for i in range(0, len(monthly_data), 6)], 
                  rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Subplot 3: Top 15 Brands by model count
        plt.subplot(2, 2, 3)
        brand_counts = bmg_df['Marka'].value_counts().head(15)
        bars = plt.barh(range(len(brand_counts)), brand_counts.values, color='steelblue')
        plt.yticks(range(len(brand_counts)), brand_counts.index)
        plt.title('En Çok Model Sayısına Sahip 15 Marka', fontsize=14, fontweight='bold')
        plt.xlabel('Model Sayısı')
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2., 
                    f'{int(width)}', ha='left', va='center', fontsize=9)
        
        # Subplot 4: Brand distribution pie chart
        plt.subplot(2, 2, 4)
        top_10_brands = bmg_df['Marka'].value_counts().head(10)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', 
                 '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43']
        
        plt.pie(top_10_brands.values, labels=top_10_brands.index, autopct='%1.1f%%', 
               startangle=90, colors=colors)
        plt.title('En Popüler 10 Markanın Dağılımı', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('charts/emisyon_analizi_genel.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # === CHART 2: Detailed Brand Analysis ===
        plt.figure(figsize=(16, 10))
        
        # Top brands analysis
        plt.subplot(2, 1, 1)
        top_20_brands = bmg_df['Marka'].value_counts().head(20)
        bars = plt.bar(range(len(top_20_brands)), top_20_brands.values, 
                      color=plt.cm.viridis(np.linspace(0, 1, len(top_20_brands))))
        plt.title('En Fazla Model Çeşitliliğine Sahip 20 Marka', fontsize=16, fontweight='bold')
        plt.xlabel('Markalar')
        plt.ylabel('Model Sayısı')
        plt.xticks(range(len(top_20_brands)), top_20_brands.index, rotation=45, ha='right')
        
        # Add value labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        # Model distribution analysis
        plt.subplot(2, 1, 2)
        
        # Calculate models per brand statistics
        models_per_brand = bmg_df.groupby('Marka')['Model'].nunique().sort_values(ascending=False).head(15)
        bars = plt.barh(range(len(models_per_brand)), models_per_brand.values, color='coral')
        plt.yticks(range(len(models_per_brand)), models_per_brand.index)
        plt.title('Markalar Bazında Benzersiz Model Sayıları (Top 15)', fontsize=16, fontweight='bold')
        plt.xlabel('Benzersiz Model Sayısı')
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2., 
                    f'{int(width)}', ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('charts/marka_detay_analizi.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # === CHART 3: Sales Trends and Growth Analysis ===
        plt.figure(figsize=(14, 10))
        
        # Calculate growth rates
        yearly_sales = emission_df.groupby('Yıl')['Adet'].sum()
        growth_rates = yearly_sales.pct_change() * 100
        
        plt.subplot(2, 2, 1)
        bars = plt.bar(yearly_sales.index, yearly_sales.values, 
                      color=['#E74C3C', '#3498DB', '#2ECC71', '#F39C12'])
        plt.title('Yıllık Satış Performansı', fontsize=14, fontweight='bold')
        plt.xlabel('Yıl')
        plt.ylabel('Toplam Satış (Adet)')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height/1000)}K', ha='center', va='bottom', fontsize=10)
        
        # Growth rate chart
        plt.subplot(2, 2, 2)
        growth_years = growth_rates.dropna()
        colors = ['green' if x > 0 else 'red' for x in growth_years.values]
        bars = plt.bar(growth_years.index, growth_years.values, color=colors, alpha=0.7)
        plt.title('Yıllık Büyüme Oranları (%)', fontsize=14, fontweight='bold')
        plt.xlabel('Yıl')
        plt.ylabel('Büyüme Oranı (%)')
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', 
                    va='bottom' if height > 0 else 'top', fontsize=10)
        
        # Seasonal analysis
        plt.subplot(2, 2, 3)
        monthly_avg = emission_df.groupby('Ay')['Adet'].mean()
        month_order = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                      'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
        monthly_avg_ordered = monthly_avg.reindex(month_order)
        
        plt.plot(range(12), monthly_avg_ordered.values, marker='o', linewidth=3, 
                markersize=8, color='purple')
        plt.title('Mevsimsel Satış Eğilimleri', fontsize=14, fontweight='bold')
        plt.xlabel('Ay')
        plt.ylabel('Ortalama Satış')
        plt.xticks(range(12), [m[:3] for m in month_order], rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Market share simulation (using available brands)
        plt.subplot(2, 2, 4)
        
        # Simulate market share based on model variety
        top_brands_share = bmg_df['Marka'].value_counts().head(8)
        total = top_brands_share.sum()
        percentages = (top_brands_share / total * 100)
        
        plt.pie(percentages.values, labels=percentages.index, autopct='%1.1f%%', 
               startangle=90)
        plt.title('Model Çeşitliliği Bazında Pazar Payı Tahmini', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('charts/satis_trend_analizi.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Try to load and analyze main emission file
        try:
            print("📈 Ana emisyon dosyası analiz ediliyor...")
            main_emission_df = pd.read_excel('Marka_Model_Emisyon Bilgisi_2021_2024.xls')
            print(f"Ana emisyon verileri: {len(main_emission_df)} kayıt")
            print(f"Sütunlar: {list(main_emission_df.columns)}")
            
            # Create additional analysis if main file loads successfully
            plt.figure(figsize=(12, 8))
            
            # Basic statistics from main file
            plt.subplot(2, 1, 1)
            plt.text(0.1, 0.8, f"📊 ANA EMİSYON VERİLERİ ANALİZİ", fontsize=20, fontweight='bold')
            plt.text(0.1, 0.6, f"Toplam Kayıt: {len(main_emission_df):,}", fontsize=14)
            plt.text(0.1, 0.5, f"Sütun Sayısı: {len(main_emission_df.columns)}", fontsize=14)
            plt.text(0.1, 0.4, f"Veri Dönemi: 2021-2024", fontsize=14)
            plt.text(0.1, 0.3, f"Analiz Tarihi: {pd.Timestamp.now().strftime('%d/%m/%Y')}", fontsize=14)
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.axis('off')
            
            plt.subplot(2, 1, 2)
            plt.text(0.1, 0.8, "📋 VERİ KAYNAKLARI:", fontsize=16, fontweight='bold')
            plt.text(0.1, 0.7, "• Aylık satış verileri (48 dönem)", fontsize=12)
            plt.text(0.1, 0.6, "• 344 otomobil markası", fontsize=12)
            plt.text(0.1, 0.5, "• 43,448 detaylı model kaydı", fontsize=12)
            plt.text(0.1, 0.4, "• ODMD resmi raporları", fontsize=12)
            plt.text(0.1, 0.3, "• Auto-data.net teknik verileri", fontsize=12)
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.axis('off')
            
            plt.tight_layout()
            plt.savefig('charts/veri_ozeti.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"⚠️  Ana emisyon dosyası işlenirken hata: {e}")
        
        print("\n✅ Tüm grafikler başarıyla oluşturuldu!")
        print("📁 Grafikler 'charts' klasöründe kaydedildi:")
        print("   📊 emisyon_analizi_genel.png - Genel analiz grafikleri")
        print("   🏭 marka_detay_analizi.png - Detaylı marka analizleri") 
        print("   📈 satis_trend_analizi.png - Satış trend analizleri")
        print("   📋 veri_ozeti.png - Veri kaynakları özeti")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_emission_charts()