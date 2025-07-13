import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['font.size'] = 11
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def analyze_multi_year_co2_emissions():
    """
    2021-2024 yılları arasındaki CO2 emisyon verilerini analiz eder
    """
    print("🚗 Çok Yıllı CO2 Emisyon Analizi Başlatılıyor...")
    print("=" * 70)
    
    # Ana dosyayı oku
    try:
        df_main = pd.read_excel('Marka_Model_Emisyon Bilgisi_2021_2024.xls', sheet_name=None)
        print(f"✅ Ana dosya başarıyla okundu! Çalışma sayfası sayısı: {len(df_main.keys())}")
        print(f"📊 Mevcut sayfalar: {list(df_main.keys())}")
    except Exception as e:
        print(f"❌ Dosya okuma hatası: {e}")
        return None
    
    # Yıllık veriler
    yearly_data = {}
    yearly_stats = {}
    all_combined_data = []
    
    # Her yıl için analiz
    for sheet_name, df in df_main.items():
        year = sheet_name
        print(f"\n📅 {year} Yılı Analiz Ediliyor...")
        print(f"   Veri boyutu: {df.shape}")
        
        # Sütun isimlerini yazdır
        print(f"   Sütunlar: {list(df.columns)}")
        
        # CO2 sütununu bul
        co2_column = None
        for col in df.columns:
            if 'co2' in str(col).lower() and 'seviyesi' in str(col).lower():
                co2_column = col
                break
        
        if not co2_column:
            print(f"   ⚠️ CO2 sütunu bulunamadı!")
            continue
            
        print(f"   CO2 sütunu: {co2_column}")
        
        # Aylık sütunları bul
        monthly_cols = []
        for col in df.columns:
            col_str = str(col).lower()
            if any(str(i) in col_str for i in range(1, 13)) and 'co2' not in col_str:
                monthly_cols.append(col)
        
        print(f"   Aylık sütunlar: {len(monthly_cols)} adet")
        
        # Veriyi işle
        processed_data = []
        for idx, row in df.iterrows():
            try:
                co2_value = row[co2_column]
                if pd.notna(co2_value) and co2_value > 0:
                    # Aylık satışları topla
                    monthly_sales = 0
                    for month_col in monthly_cols:
                        if pd.notna(row[month_col]):
                            monthly_sales += row[month_col]
                    
                    if monthly_sales > 0:  # Sadece satışı olan verileri al
                        processed_data.append({
                            'year': year,
                            'marka': row.get('Marka', 'Bilinmeyen'),
                            'model': row.get('Model', 'Bilinmeyen'),
                            'co2_emisyon': co2_value,
                            'total_sales': monthly_sales
                        })
            except Exception as e:
                continue
        
        # Yıllık istatistikler
        if processed_data:
            year_df = pd.DataFrame(processed_data)
            yearly_data[year] = year_df
            
            # Ağırlıklı ortalama CO2 hesapla
            total_weighted_co2 = (year_df['co2_emisyon'] * year_df['total_sales']).sum()
            total_sales = year_df['total_sales'].sum()
            weighted_avg_co2 = total_weighted_co2 / total_sales if total_sales > 0 else 0
            
            yearly_stats[year] = {
                'total_vehicles': int(total_sales),
                'total_records': len(year_df),
                'unique_brands': year_df['marka'].nunique(),
                'unique_models': year_df['model'].nunique(),
                'weighted_avg_co2': weighted_avg_co2,
                'min_co2': year_df['co2_emisyon'].min(),
                'max_co2': year_df['co2_emisyon'].max(),
                'median_co2': year_df['co2_emisyon'].median()
            }
            
            # Tüm verileri birleştir
            all_combined_data.extend(processed_data)
            
            print(f"   ✅ {len(processed_data):,} kayıt işlendi")
            print(f"   📊 Toplam satış: {total_sales:,.0f}")
            print(f"   🌡️ Ağırlıklı ortalama CO2: {weighted_avg_co2:.1f} g/km")
    
    # Birleştirilmiş veri analizi
    if all_combined_data:
        combined_df = pd.DataFrame(all_combined_data)
        print(f"\n📊 Genel İstatistikler (2021-2024):")
        print(f"   Toplam kayıt: {len(combined_df):,}")
        print(f"   Toplam satış: {combined_df['total_sales'].sum():,.0f}")
        print(f"   Benzersiz marka: {combined_df['marka'].nunique()}")
        print(f"   Benzersiz model: {combined_df['model'].nunique()}")
        
        return yearly_data, yearly_stats, combined_df
    
    return None

def create_co2_categories(co2_value):
    """CO2 değerini kategoriye ayırır"""
    if co2_value <= 120:
        return "Mükemmel (0-120)"
    elif co2_value <= 150:
        return "İyi (121-150)"
    elif co2_value <= 180:
        return "Orta (151-180)"
    elif co2_value <= 200:
        return "Zayıf (181-200)"
    else:
        return "Kötü (200+)"

def analyze_trends_and_patterns(yearly_data, yearly_stats):
    """Yıllık trendleri ve desenleri analiz eder"""
    print("\n📈 Trend Analizi:")
    print("=" * 50)
    
    # Yıllık CO2 trendi
    years = sorted(yearly_stats.keys())
    co2_trends = []
    
    for year in years:
        stats = yearly_stats[year]
        co2_trends.append({
            'year': year,
            'weighted_avg_co2': stats['weighted_avg_co2'],
            'total_vehicles': stats['total_vehicles'],
            'unique_brands': stats['unique_brands'],
            'unique_models': stats['unique_models']
        })
    
    trends_df = pd.DataFrame(co2_trends)
    
    # CO2 trend yüzdesi
    if len(trends_df) > 1:
        co2_change = ((trends_df['weighted_avg_co2'].iloc[-1] - trends_df['weighted_avg_co2'].iloc[0]) 
                     / trends_df['weighted_avg_co2'].iloc[0]) * 100
        print(f"🌡️ CO2 Emisyon Trendi: {co2_change:+.1f}%")
    
    # Satış trendi
    if len(trends_df) > 1:
        sales_change = ((trends_df['total_vehicles'].iloc[-1] - trends_df['total_vehicles'].iloc[0]) 
                       / trends_df['total_vehicles'].iloc[0]) * 100
        print(f"📊 Satış Trendi: {sales_change:+.1f}%")
    
    return trends_df

def create_visualizations(yearly_data, yearly_stats, combined_df):
    """Görselleştirmeler oluşturur"""
    print("\n🎨 Görselleştirmeler Oluşturuluyor...")
    
    # Grafik boyutlarını ayarla
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('2021-2024 Türkiye Otomotiv Sektörü CO2 Emisyon Analizi', fontsize=16, fontweight='bold')
    
    # 1. Yıllık CO2 trendi
    years = sorted(yearly_stats.keys())
    co2_values = [yearly_stats[year]['weighted_avg_co2'] for year in years]
    
    axes[0, 0].plot(years, co2_values, marker='o', linewidth=3, markersize=8, color='#2E86AB')
    axes[0, 0].set_title('Yıllık Ağırlıklı Ortalama CO2 Emisyonu', fontweight='bold')
    axes[0, 0].set_ylabel('CO2 Emisyonu (g/km)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Yıllık satış trendi
    sales_values = [yearly_stats[year]['total_vehicles'] for year in years]
    axes[0, 1].bar(years, sales_values, color='#A23B72', alpha=0.7)
    axes[0, 1].set_title('Yıllık Toplam Araç Satışı', fontweight='bold')
    axes[0, 1].set_ylabel('Satış Adedi')
    
    # 3. CO2 kategorileri dağılımı
    combined_df['co2_category'] = combined_df['co2_emisyon'].apply(create_co2_categories)
    category_counts = combined_df.groupby('co2_category')['total_sales'].sum().sort_values(ascending=False)
    
    colors = ['#27AE60', '#F39C12', '#E67E22', '#E74C3C', '#8E44AD']
    axes[1, 0].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
    axes[1, 0].set_title('CO2 Kategorileri Dağılımı (2021-2024)', fontweight='bold')
    
    # 4. En çok satan 10 marka
    top_brands = combined_df.groupby('marka')['total_sales'].sum().sort_values(ascending=False).head(10)
    axes[1, 1].barh(range(len(top_brands)), top_brands.values, color='#16A085')
    axes[1, 1].set_yticks(range(len(top_brands)))
    axes[1, 1].set_yticklabels(top_brands.index)
    axes[1, 1].set_title('En Çok Satan 10 Marka (2021-2024)', fontweight='bold')
    axes[1, 1].set_xlabel('Toplam Satış')
    
    plt.tight_layout()
    plt.savefig('multi_year_co2_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Grafik kaydedildi: multi_year_co2_analysis.png")

def generate_detailed_report(yearly_data, yearly_stats, combined_df):
    """Detaylı analiz raporu üretir"""
    print("\n📋 Detaylı Rapor Oluşturuluyor...")
    
    # Marka bazında analiz
    brand_analysis = {}
    for year, data in yearly_data.items():
        brand_stats = data.groupby('marka').agg({
            'co2_emisyon': ['mean', 'std'],
            'total_sales': 'sum'
        }).round(2)
        brand_analysis[year] = brand_stats
    
    # En iyi ve en kötü performans gösteren markalar
    overall_brand_performance = combined_df.groupby('marka').agg({
        'co2_emisyon': lambda x: np.average(x, weights=combined_df.loc[x.index, 'total_sales']),
        'total_sales': 'sum'
    }).round(2)
    
    overall_brand_performance.columns = ['weighted_avg_co2', 'total_sales']
    overall_brand_performance = overall_brand_performance.sort_values('weighted_avg_co2')
    
    # CO2 kategorileri detaylı analiz
    co2_categories = combined_df.copy()
    co2_categories['co2_category'] = co2_categories['co2_emisyon'].apply(create_co2_categories)
    
    category_analysis = co2_categories.groupby('co2_category').agg({
        'total_sales': 'sum',
        'co2_emisyon': ['mean', 'min', 'max']
    }).round(2)
    
    return {
        'brand_analysis': brand_analysis,
        'overall_brand_performance': overall_brand_performance,
        'category_analysis': category_analysis
    }

def main():
    """Ana fonksiyon"""
    print("🚀 Çok Yıllı CO2 Emisyon Analizi Başlatılıyor...")
    print("=" * 70)
    
    # Veri analizi
    result = analyze_multi_year_co2_emissions()
    
    if result:
        yearly_data, yearly_stats, combined_df = result
        
        # Trend analizi
        trends_df = analyze_trends_and_patterns(yearly_data, yearly_stats)
        
        # Görselleştirmeler
        create_visualizations(yearly_data, yearly_stats, combined_df)
        
        # Detaylı rapor
        detailed_report = generate_detailed_report(yearly_data, yearly_stats, combined_df)
        
        print("\n✅ Analiz tamamlandı!")
        print("\nYıllık İstatistikler:")
        for year, stats in yearly_stats.items():
            print(f"\n📅 {year}:")
            print(f"   Toplam araç: {stats['total_vehicles']:,}")
            print(f"   Benzersiz marka: {stats['unique_brands']}")
            print(f"   Benzersiz model: {stats['unique_models']}")
            print(f"   Ağırlıklı ortalama CO2: {stats['weighted_avg_co2']:.1f} g/km")
        
        return yearly_data, yearly_stats, combined_df, detailed_report
    else:
        print("❌ Analiz başarısız oldu!")
        return None

if __name__ == "__main__":
    main()