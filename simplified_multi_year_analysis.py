import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['figure.facecolor'] = 'white'

def analyze_multi_year_data():
    """2021-2024 yılları arasındaki CO2 emisyon verilerini analiz eder"""
    print("🚗 Çok Yıllı CO2 Emisyon Analizi")
    print("=" * 60)
    
    try:
        # Ana emisyon dosyasını oku
        df_main = pd.read_excel('Marka_Model_Emisyon Bilgisi_2021_2024.xls', sheet_name=None)
        print(f"✅ Ana dosya başarıyla okundu! Sayfa sayısı: {len(df_main.keys())}")
        
        # Tüm yılları birleştir
        all_data = []
        yearly_stats = {}
        
        for year_sheet, df in df_main.items():
            year = year_sheet
            print(f"\n📅 {year} yılı analiz ediliyor...")
            print(f"   Boyut: {df.shape}")
            
            # Sütunları temizle ve standartlaştır
            df_clean = df.copy()
            
            # CO2 seviyesi sütununu bul
            co2_column = None
            for col in df_clean.columns:
                if 'co2' in str(col).lower() and 'seviyesi' in str(col).lower():
                    co2_column = col
                    break
            
            if co2_column:
                print(f"   CO2 sütunu bulundu: {co2_column}")
                
                # Aylık sütunları bul
                monthly_cols = [col for col in df_clean.columns if any(str(i) in str(col) for i in range(1, 13)) and 'co2' not in str(col).lower()]
                
                # Her satır için CO2 seviyesi ve aylık satışları al
                for idx, row in df_clean.iterrows():
                    try:
                        co2_value = row[co2_column]
                        if pd.notna(co2_value) and str(co2_value).replace('.', '').replace(',', '').isdigit():
                            co2_float = float(str(co2_value).replace(',', '.'))
                            
                            # CO2 kategorisini belirle
                            if co2_float <= 120:
                                co2_category = "0-120 g/km"
                            elif co2_float <= 150:
                                co2_category = "121-150 g/km"
                            elif co2_float <= 180:
                                co2_category = "151-180 g/km"
                            elif co2_float <= 200:
                                co2_category = "181-200 g/km"
                            else:
                                co2_category = "200+ g/km"
                            
                            # Aylık satışları topla
                            for month_col in monthly_cols:
                                if month_col in row and pd.notna(row[month_col]):
                                    try:
                                        sales = float(row[month_col])
                                        if sales > 0:
                                            # Ay numarasını çıkar
                                            month_num = None
                                            for i in range(1, 13):
                                                if str(i) in month_col:
                                                    month_num = i
                                                    break
                                            
                                            if month_num:
                                                all_data.append({
                                                    'Yıl': int(year),
                                                    'Ay': month_num,
                                                    'Marka': str(row.get('Marka / Marka', 'Bilinmeyen')),
                                                    'Model': str(row.get('Model / Model', 'Bilinmeyen')),
                                                    'CO2_Seviyesi': co2_float,
                                                    'CO2_Kategorisi': co2_category,
                                                    'Satış_Adedi': sales
                                                })
                                    except:
                                        continue
                    except:
                        continue
                
                # Yıllık istatistikler
                year_total = df_clean[monthly_cols].sum().sum() if monthly_cols else 0
                yearly_stats[year] = {
                    'total_sales': year_total,
                    'models': len(df_clean),
                    'brands': len(df_clean['Marka / Marka'].unique()) if 'Marka / Marka' in df_clean.columns else 0
                }
                
                print(f"   ✅ {year}: {year_total:,.0f} toplam satış, {yearly_stats[year]['models']} model")
        
        if not all_data:
            print("❌ Veri işlenemedi!")
            return None
        
        # DataFrame oluştur
        df_final = pd.DataFrame(all_data)
        print(f"\n📊 Birleştirilmiş veri seti: {len(df_final):,} kayıt")
        print(f"📅 Yıl aralığı: {df_final['Yıl'].min()} - {df_final['Yıl'].max()}")
        print(f"🚗 Toplam satış: {df_final['Satış_Adedi'].sum():,.0f}")
        
        return df_final, yearly_stats
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def calculate_yearly_statistics(df):
    """Yıllık istatistikleri hesaplar"""
    yearly_analysis = {}
    
    for year in sorted(df['Yıl'].unique()):
        year_data = df[df['Yıl'] == year]
        
        # Ağırlıklı ortalama CO2 hesapla
        total_weighted_co2 = (year_data['CO2_Seviyesi'] * year_data['Satış_Adedi']).sum()
        total_sales = year_data['Satış_Adedi'].sum()
        weighted_avg_co2 = total_weighted_co2 / total_sales if total_sales > 0 else 0
        
        # CO2 kategorileri dağılımı
        category_distribution = year_data.groupby('CO2_Kategorisi')['Satış_Adedi'].sum()
        category_percentages = (category_distribution / total_sales * 100).round(1)
        
        yearly_analysis[year] = {
            'total_sales': int(total_sales),
            'weighted_avg_co2': round(weighted_avg_co2, 1),
            'min_co2': year_data['CO2_Seviyesi'].min(),
            'max_co2': year_data['CO2_Seviyesi'].max(),
            'unique_brands': year_data['Marka'].nunique(),
            'unique_models': year_data['Model'].nunique(),
            'category_distribution': category_distribution.to_dict(),
            'category_percentages': category_percentages.to_dict()
        }
    
    return yearly_analysis

def create_summary_visualizations(df, yearly_stats):
    """Özet görselleştirmeler oluşturur"""
    print("\n🎨 Görselleştirmeler oluşturuluyor...")
    
    # Grafik boyutlarını ayarla
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Türkiye Otomotiv Sektörü CO2 Emisyon Analizi (2021-2024)', fontsize=14, fontweight='bold')
    
    # Yıllık istatistikleri hesapla
    yearly_analysis = calculate_yearly_statistics(df)
    
    # 1. Yıllık ağırlıklı ortalama CO2 trendi
    years = sorted(yearly_analysis.keys())
    co2_values = [yearly_analysis[year]['weighted_avg_co2'] for year in years]
    
    axes[0, 0].plot(years, co2_values, marker='o', linewidth=2, markersize=6, color='#2E86AB')
    axes[0, 0].set_title('Yıllık Ağırlıklı Ortalama CO2 Emisyonu', fontweight='bold')
    axes[0, 0].set_ylabel('CO2 Emisyonu (g/km)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Yıllık satış trendi
    sales_values = [yearly_analysis[year]['total_sales'] for year in years]
    axes[0, 1].bar(years, sales_values, color='#A23B72', alpha=0.7)
    axes[0, 1].set_title('Yıllık Toplam Araç Satışı', fontweight='bold')
    axes[0, 1].set_ylabel('Satış Adedi')
    
    # 3. CO2 kategorileri genel dağılımı
    category_totals = df.groupby('CO2_Kategorisi')['Satış_Adedi'].sum().sort_index()
    colors = ['#27AE60', '#F39C12', '#E67E22', '#E74C3C', '#8E44AD']
    axes[1, 0].pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
    axes[1, 0].set_title('CO2 Kategorileri Dağılımı (2021-2024)', fontweight='bold')
    
    # 4. En çok satan markalar
    top_brands = df.groupby('Marka')['Satış_Adedi'].sum().sort_values(ascending=False).head(10)
    axes[1, 1].barh(range(len(top_brands)), top_brands.values, color='#16A085')
    axes[1, 1].set_yticks(range(len(top_brands)))
    axes[1, 1].set_yticklabels(top_brands.index)
    axes[1, 1].set_title('En Çok Satan 10 Marka', fontweight='bold')
    axes[1, 1].set_xlabel('Toplam Satış')
    
    plt.tight_layout()
    plt.savefig('turkiye_otomotiv_co2_analizi_2021_2024.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Grafik kaydedildi: turkiye_otomotiv_co2_analizi_2021_2024.png")
    
    return yearly_analysis

def print_detailed_statistics(yearly_analysis):
    """Detaylı istatistikleri yazdırır"""
    print("\n📊 Detaylı İstatistikler:")
    print("=" * 60)
    
    for year, stats in yearly_analysis.items():
        print(f"\n📅 {year} Yılı:")
        print(f"   Toplam Satış: {stats['total_sales']:,} araç")
        print(f"   Ağırlıklı Ortalama CO2: {stats['weighted_avg_co2']} g/km")
        print(f"   En Düşük CO2: {stats['min_co2']} g/km")
        print(f"   En Yüksek CO2: {stats['max_co2']} g/km")
        print(f"   Benzersiz Marka: {stats['unique_brands']}")
        print(f"   Benzersiz Model: {stats['unique_models']}")
        
        print(f"   CO2 Kategorileri:")
        for category, percentage in stats['category_percentages'].items():
            sales = stats['category_distribution'][category]
            print(f"     {category}: {sales:,} araç ({percentage}%)")

def main():
    """Ana fonksiyon"""
    # Veri analizi
    result = analyze_multi_year_data()
    
    if result:
        df_final, yearly_stats = result
        
        # Görselleştirmeler
        yearly_analysis = create_summary_visualizations(df_final, yearly_stats)
        
        # Detaylı istatistikler
        print_detailed_statistics(yearly_analysis)
        
        print("\n✅ Analiz tamamlandı!")
        
        return df_final, yearly_analysis
    else:
        print("❌ Analiz başarısız oldu!")
        return None

if __name__ == "__main__":
    main()