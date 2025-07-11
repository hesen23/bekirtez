import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği ve grafik ayarları
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['figure.facecolor'] = 'white'

def comprehensive_co2_analysis():
    print("🚗 Kapsamlı CO2 Emisyon Analizi Başlatılıyor...")
    print("=" * 60)
    
    try:
        # Ana emisyon dosyasını oku
        print("📂 Ana emisyon dosyası okunuyor...")
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
                if 'co2' in str(col).lower():
                    co2_column = col
                    break
            
            if co2_column:
                print(f"   CO2 sütunu bulundu: {co2_column}")
                
                # Aylık sütunları bul
                monthly_cols = [col for col in df_clean.columns if any(str(i) in str(col) for i in range(1, 13))]
                
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
                                                     'Yıl': int(str(year)),
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
            print("❌ Veri işlenemedi, demo grafik oluşturuluyor...")
            create_demo_co2_analysis()
            return
        
        # DataFrame oluştur
        df_final = pd.DataFrame(all_data)
        print(f"\n📊 Birleştirilmiş veri seti: {len(df_final):,} kayıt")
        print(f"📅 Yıl aralığı: {df_final['Yıl'].min()} - {df_final['Yıl'].max()}")
        print(f"🚗 Toplam satış: {df_final['Satış_Adedi'].sum():,.0f}")
        
        # Grafikleri oluştur
        create_comprehensive_visualizations(df_final, yearly_stats)
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        print("🎨 Demo grafik oluşturuluyor...")
        create_demo_co2_analysis()

def create_comprehensive_visualizations(df, yearly_stats):
    """Kapsamlı CO2 emisyon görselleştirmeleri"""
    print("\n🎨 Kapsamlı grafikler oluşturuluyor...")
    
    # Ana grafik seti
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Yıllık CO2 Kategorileri Dağılımı (Stacked Bar)
    ax1 = plt.subplot(3, 3, 1)
    yearly_category = df.groupby(['Yıl', 'CO2_Kategorisi'])['Satış_Adedi'].sum().unstack(fill_value=0)
    colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
    yearly_category.plot(kind='bar', stacked=True, ax=ax1, color=colors[:len(yearly_category.columns)])
    ax1.set_title('📊 Yıllık CO2 Kategorileri Dağılımı', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Yıl')
    ax1.set_ylabel('Satış Adedi')
    ax1.legend(title='CO2 Kategorisi', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.tick_params(axis='x', rotation=0)
    
    # 2. Aylık CO2 Emisyon Trendi
    ax2 = plt.subplot(3, 3, 2)
    monthly_trend = df.groupby(['Yıl', 'Ay'])['Satış_Adedi'].sum().reset_index()
    monthly_trend['Tarih'] = pd.to_datetime(monthly_trend[['Yıl', 'Ay']].assign(Day=1))
    ax2.plot(monthly_trend['Tarih'], monthly_trend['Satış_Adedi'], marker='o', linewidth=2, markersize=4)
    ax2.set_title('📈 Aylık Satış Trendi', fontweight='bold', fontsize=12)
    ax2.set_xlabel('Tarih')
    ax2.set_ylabel('Toplam Satış')
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. CO2 Kategorileri Pasta Grafiği
    ax3 = plt.subplot(3, 3, 3)
    category_totals = df.groupby('CO2_Kategorisi')['Satış_Adedi'].sum()
    wedges, texts, autotexts = ax3.pie(category_totals.values, labels=category_totals.index, 
                                      autopct='%1.1f%%', colors=colors[:len(category_totals)])
    ax3.set_title('🎯 Toplam CO2 Kategorileri Dağılımı', fontweight='bold', fontsize=12)
    
    # 4. En Çok Satan Markalar (CO2 bazında)
    ax4 = plt.subplot(3, 3, 4)
    top_brands = df.groupby('Marka')['Satış_Adedi'].sum().nlargest(10)
    bars = ax4.barh(range(len(top_brands)), top_brands.values, color='blue', alpha=0.7)
    ax4.set_yticks(range(len(top_brands)))
    ax4.set_yticklabels(top_brands.index)
    ax4.set_title('🏆 En Çok Satan 10 Marka', fontweight='bold', fontsize=12)
    ax4.set_xlabel('Toplam Satış')
    
    # Değerleri barların yanına yaz
    for i, (bar, value) in enumerate(zip(bars, top_brands.values)):
        ax4.text(bar.get_width() + max(top_brands)*0.01, bar.get_y() + bar.get_height()/2.,
                f'{value:,.0f}', ha='left', va='center', fontsize=8)
    
    # 5. Ortalama CO2 Seviyesi Trendi
    ax5 = plt.subplot(3, 3, 5)
    # Ağırlıklı ortalama CO2 hesapla
    weighted_co2 = df.groupby(['Yıl', 'Ay']).apply(
        lambda x: np.average(x['CO2_Seviyesi'], weights=x['Satış_Adedi'])
    ).reset_index()
    weighted_co2.columns = ['Yıl', 'Ay', 'Ortalama_CO2']
    weighted_co2['Tarih'] = pd.to_datetime(weighted_co2[['Yıl', 'Ay']].assign(Day=1))
    
    ax5.plot(weighted_co2['Tarih'], weighted_co2['Ortalama_CO2'], 
             marker='s', linewidth=2, color='red', markersize=4)
    ax5.set_title('📉 Ağırlıklı Ortalama CO2 Trendi', fontweight='bold', fontsize=12)
    ax5.set_xlabel('Tarih')
    ax5.set_ylabel('Ortalama CO2 (g/km)')
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(axis='x', rotation=45)
    
    # 6. Yıllık Karşılaştırma
    ax6 = plt.subplot(3, 3, 6)
    yearly_total = df.groupby('Yıl')['Satış_Adedi'].sum()
    bars = ax6.bar(yearly_total.index, yearly_total.values, 
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'][:len(yearly_total)])
    ax6.set_title('📊 Yıllık Toplam Satış', fontweight='bold', fontsize=12)
    ax6.set_xlabel('Yıl')
    ax6.set_ylabel('Toplam Satış')
    
    # Değerleri barların üstüne yaz
    for bar, value in zip(bars, yearly_total.values):
        ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(yearly_total)*0.01,
                f'{value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 7. CO2 Seviyesi Dağılımı (Histogram)
    ax7 = plt.subplot(3, 3, 7)
    # Satış ağırlıklı histogram
    weights = df['Satış_Adedi'] / df['Satış_Adedi'].sum()
    ax7.hist(df['CO2_Seviyesi'], bins=50, weights=weights, color='purple', alpha=0.7, edgecolor='black')
    ax7.set_title('📈 CO2 Seviyesi Dağılımı (Ağırlıklı)', fontweight='bold', fontsize=12)
    ax7.set_xlabel('CO2 Seviyesi (g/km)')
    ax7.set_ylabel('Ağırlıklı Frekans')
    ax7.grid(True, alpha=0.3)
    
    # İstatistikler ekle
    weighted_mean = np.average(df['CO2_Seviyesi'], weights=df['Satış_Adedi'])
    ax7.axvline(weighted_mean, color='red', linestyle='--', linewidth=2, 
                label=f'Ağırlıklı Ort: {weighted_mean:.1f} g/km')
    ax7.legend()
    
    # 8. En Düşük/Yüksek Emisyonlu Modeller
    ax8 = plt.subplot(3, 3, 8)
    model_emissions = df.groupby(['Marka', 'Model']).agg({
        'CO2_Seviyesi': 'mean',
        'Satış_Adedi': 'sum'
    }).reset_index()
    
    # En çok satan 20 model arasından en düşük emisyonlular
    top_models = model_emissions.nlargest(20, 'Satış_Adedi')
    eco_models = top_models.nsmallest(8, 'CO2_Seviyesi')
    
    bars = ax8.barh(range(len(eco_models)), eco_models['CO2_Seviyesi'], color='green', alpha=0.8)
    ax8.set_yticks(range(len(eco_models)))
    ax8.set_yticklabels([f"{row['Marka']}\n{row['Model']}" for _, row in eco_models.iterrows()], fontsize=8)
    ax8.set_title('🌱 En Eco-Friendly Modeller\n(Popüler olanlar arasında)', fontweight='bold', fontsize=12)
    ax8.set_xlabel('Ortalama CO2 (g/km)')
    
    # 9. Mevsimsel Analiz
    ax9 = plt.subplot(3, 3, 9)
    df['Mevsim'] = df['Ay'].map({12: 'Kış', 1: 'Kış', 2: 'Kış',
                                3: 'İlkbahar', 4: 'İlkbahar', 5: 'İlkbahar',
                                6: 'Yaz', 7: 'Yaz', 8: 'Yaz',
                                9: 'Sonbahar', 10: 'Sonbahar', 11: 'Sonbahar'})
    
    seasonal_data = df.groupby(['Mevsim', 'CO2_Kategorisi'])['Satış_Adedi'].sum().unstack(fill_value=0)
    seasonal_data.plot(kind='bar', stacked=True, ax=ax9, color=colors[:len(seasonal_data.columns)])
    ax9.set_title('🍂 Mevsimsel CO2 Dağılımı', fontweight='bold', fontsize=12)
    ax9.set_xlabel('Mevsim')
    ax9.set_ylabel('Satış Adedi')
    ax9.legend(title='CO2 Kategorisi', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax9.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('comprehensive_co2_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Özet istatistikler yazdır
    print_comprehensive_stats(df)

def print_comprehensive_stats(df):
    """Kapsamlı istatistikleri yazdır"""
    print("\n" + "="*80)
    print("📊 KAPSAMLI CO2 EMİSYON ANALİZİ - ÖZET RAPOR")
    print("="*80)
    
    print(f"\n📅 ANALİZ DÖNEMİ: {df['Yıl'].min()} - {df['Yıl'].max()}")
    print(f"🚗 TOPLAM SATIŞ: {df['Satış_Adedi'].sum():,.0f} araç")
    print(f"🏭 MARKA SAYISI: {df['Marka'].nunique()} marka")
    print(f"🚙 MODEL SAYISI: {df['Model'].nunique()} model")
    
    # Yıllık karşılaştırma
    print(f"\n📈 YILLIK KARŞILAŞTIRMA:")
    yearly_sales = df.groupby('Yıl')['Satış_Adedi'].sum()
    for year, sales in yearly_sales.items():
        change = ""
        if year > yearly_sales.index.min():
            prev_sales = yearly_sales[year-1]
            pct_change = ((sales - prev_sales) / prev_sales) * 100
            change = f" ({pct_change:+.1f}%)"
        print(f"   {year}: {sales:>10,.0f} araç{change}")
    
    # CO2 kategorileri
    print(f"\n🎯 CO2 KATEGORİLERİ DAĞILIMI:")
    category_stats = df.groupby('CO2_Kategorisi')['Satış_Adedi'].sum().sort_values(ascending=False)
    total_sales = df['Satış_Adedi'].sum()
    for category, sales in category_stats.items():
        percentage = (sales / total_sales) * 100
        print(f"   {category:<15}: {sales:>10,.0f} ({percentage:>5.1f}%)")
    
    # En başarılı markalar
    print(f"\n🏆 EN BAŞARILI MARKALAR:")
    top_brands = df.groupby('Marka')['Satış_Adedi'].sum().nlargest(10)
    for i, (brand, sales) in enumerate(top_brands.items(), 1):
        market_share = (sales / total_sales) * 100
        print(f"   {i:>2}. {brand:<15}: {sales:>10,.0f} ({market_share:>4.1f}%)")
    
    # Emisyon istatistikleri
    weighted_avg_co2 = np.average(df['CO2_Seviyesi'], weights=df['Satış_Adedi'])
    print(f"\n🌡️ EMİSYON İSTATİSTİKLERİ:")
    print(f"   Ağırlıklı Ortalama CO2: {weighted_avg_co2:.1f} g/km")
    print(f"   En Düşük CO2: {df['CO2_Seviyesi'].min():.1f} g/km")
    print(f"   En Yüksek CO2: {df['CO2_Seviyesi'].max():.1f} g/km")
    
    # Trend analizi
    yearly_avg_co2 = df.groupby('Yıl').apply(
        lambda x: np.average(x['CO2_Seviyesi'], weights=x['Satış_Adedi'])
    )
    print(f"\n📉 YILLIK ORTALAMA CO2 TRENDİ:")
    for year, avg_co2 in yearly_avg_co2.items():
        trend = ""
        if year > yearly_avg_co2.index.min():
            prev_co2 = yearly_avg_co2[year-1]
            change = avg_co2 - prev_co2
            trend = f" ({change:+.1f} g/km)"
        print(f"   {year}: {avg_co2:>6.1f} g/km{trend}")

def create_demo_co2_analysis():
    """Demo CO2 analizi oluştur"""
    print("\n🎨 Demo CO2 analizi oluşturuluyor...")
    
    # Örnek veri oluştur
    years = [2021, 2022, 2023, 2024]
    months = list(range(1, 13))
    
    # CO2 emisyon kategorileri
    categories = ['0-120 g/km', '121-150 g/km', '151-180 g/km', '181-200 g/km', '200+ g/km']
    
    # Rastgele ancak gerçekçi veriler
    np.random.seed(42)
    data = []
    
    for year in years:
        for month in months:
            for category in categories:
                # Kategoriye göre farklı ağırlıklar
                if '0-120' in category:
                    base = 15000
                elif '121-150' in category:
                    base = 25000
                elif '151-180' in category:
                    base = 20000
                elif '181-200' in category:
                    base = 10000
                else:
                    base = 5000
                    
                # Yıl trendli artış ve mevsimsel değişim
                trend_factor = 1 + (year - 2021) * 0.05
                seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * month / 12)
                noise = np.random.normal(1, 0.1)
                
                value = int(base * trend_factor * seasonal_factor * noise)
                data.append({
                    'Yıl': year,
                    'Ay': month, 
                    'Emisyon_Kategorisi': category,
                    'Araç_Sayısı': max(0, value)
                })
    
    df = pd.DataFrame(data)
    
    # Grafik oluştur
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('🚗 CO2 Emisyon Analizi (Demo Veriler)', fontsize=16, fontweight='bold')
    
    # 1. Yıllık trend
    ax1 = axes[0, 0]
    yearly_total = df.groupby('Yıl')['Araç_Sayısı'].sum()
    bars = ax1.bar(yearly_total.index, yearly_total.values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax1.set_title('📈 Yıllık Toplam CO2 Emisyonu', fontweight='bold')
    ax1.set_xlabel('Yıl')
    ax1.set_ylabel('Toplam Araç Sayısı')
    
    # Değerleri barların üstüne yaz
    for bar, value in zip(bars, yearly_total.values):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(yearly_total)*0.01,
                f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Kategori dağılımı
    ax2 = axes[0, 1]
    category_total = df.groupby('Emisyon_Kategorisi')['Araç_Sayısı'].sum().sort_values(ascending=True)
    colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
    bars = ax2.barh(category_total.index, category_total.values, color=colors)
    ax2.set_title('🎯 CO2 Emisyon Kategorileri Dağılımı', fontweight='bold')
    ax2.set_xlabel('Toplam Araç Sayısı')
    
    # 3. Aylık trend (2023 için)
    ax3 = axes[1, 0]
    monthly_2023 = df[df['Yıl'] == 2023].groupby('Ay')['Araç_Sayısı'].sum()
    ax3.plot(monthly_2023.index, monthly_2023.values, marker='o', linewidth=3, markersize=8, color='red')
    ax3.set_title('📊 2023 Yılı Aylık CO2 Emisyon Trendi', fontweight='bold')
    ax3.set_xlabel('Ay')
    ax3.set_ylabel('Araç Sayısı')
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(range(1, 13))
    
    # 4. Kategori bazında yıllık karşılaştırma
    ax4 = axes[1, 1]
    pivot_data = df.pivot_table(values='Araç_Sayısı', index='Emisyon_Kategorisi', columns='Yıl', aggfunc='sum')
    pivot_data.plot(kind='bar', ax=ax4, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax4.set_title('📈 Kategori Bazında Yıllık Karşılaştırma', fontweight='bold')
    ax4.set_xlabel('CO2 Emisyon Kategorisi')
    ax4.set_ylabel('Araç Sayısı')
    ax4.legend(title='Yıl')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('co2_emission_demo.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Özet rapor
    print("\n📊 DEMO VERİ ÖZETİ:")
    print("="*50)
    print(f"📅 Analiz Dönemi: 2021-2024")
    print(f"🎯 Emisyon Kategorileri: {len(categories)}")
    print(f"📈 Toplam Veri Noktası: {len(df):,}")
    print(f"🚗 Toplam Araç: {df['Araç_Sayısı'].sum():,}")
    print(f"📊 Yıllık Ortalama: {df.groupby('Yıl')['Araç_Sayısı'].sum().mean():,.0f}")
    
    print("\n🎯 Kategori Bazında Dağılım:")
    for cat, total in category_total.items():
        percentage = (total / df['Araç_Sayısı'].sum()) * 100
        print(f"{cat:<15}: {total:>8,} ({percentage:>5.1f}%)")

if __name__ == "__main__":
    comprehensive_co2_analysis()