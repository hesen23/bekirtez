import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Grafik ayarları
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['figure.facecolor'] = 'white'

def main():
    print("🚗 CO2 Emisyon Analizi Başlatılıyor...")
    
    try:
        # Ana emisyon dosyasını oku
        print("📂 Ana emisyon dosyası okunuyor...")
        df_main = pd.read_excel('Marka_Model_Emisyon Bilgisi_2021_2024.xls', sheet_name=None)
        print(f"✅ Ana dosya başarıyla okundu! Sayfa sayısı: {len(df_main.keys())}")
        
        # İlk yılı analiz et (2021)
        df_2021 = df_main['2021']
        print(f"\n📅 2021 verisi analiz ediliyor...")
        print(f"Boyut: {df_2021.shape}")
        print(f"Sütunlar: {list(df_2021.columns)}")
        
        # Aylık satış verilerini al
        monthly_cols = [col for col in df_2021.columns if any(str(i) in str(col) for i in range(1, 13))]
        print(f"Aylık sütunlar: {monthly_cols}")
        
        # CO2 verilerini hazırla
        co2_data = []
        
        for idx, row in df_2021.iterrows():
            try:
                co2_value = row['Emisyon Kontrol Seviyesi / CO2 Seviyesi (g/km ortalama)']
                if pd.notna(co2_value):
                    # CO2 değerini temizle
                    co2_clean = str(co2_value).replace(',', '.')
                    if co2_clean.replace('.', '').isdigit():
                        co2_float = float(co2_clean)
                        
                        # Aylık satışları topla
                        total_sales = 0
                        for month_col in monthly_cols:
                            if pd.notna(row[month_col]):
                                total_sales += float(row[month_col])
                        
                        if total_sales > 0:
                            co2_data.append({
                                'Marka': str(row['Marka / Marka']),
                                'Model': str(row['Model / Model']),
                                'CO2': co2_float,
                                'Satış': total_sales
                            })
            except:
                continue
        
        # DataFrame oluştur
        df_co2 = pd.DataFrame(co2_data)
        print(f"\n📊 CO2 veri seti hazır: {len(df_co2)} kayıt")
        
        if len(df_co2) == 0:
            print("❌ CO2 verisi bulunamadı, demo grafik oluşturuluyor...")
            create_demo_graphs()
            return
        
        # CO2 kategorilerini oluştur
        df_co2['CO2_Kategori'] = pd.cut(df_co2['CO2'], 
                                       bins=[0, 120, 150, 180, 200, float('inf')],
                                       labels=['0-120 g/km', '121-150 g/km', '151-180 g/km', 
                                              '181-200 g/km', '200+ g/km'])
        
        # Grafikler oluştur
        create_co2_graphs(df_co2)
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        print("🎨 Demo grafik oluşturuluyor...")
        create_demo_graphs()

def create_co2_graphs(df):
    """CO2 emisyon grafiklerini oluştur"""
    print("\n🎨 CO2 emisyon grafikleri oluşturuluyor...")
    
    # Ana grafik
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('🚗 CO2 Emisyon Analizi - 2021 Yılı', fontsize=16, fontweight='bold')
    
    # 1. CO2 Kategorileri Dağılımı
    ax1 = axes[0, 0]
    category_counts = df.groupby('CO2_Kategori')['Satış'].sum()
    colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
    bars = ax1.bar(range(len(category_counts)), category_counts.values, color=colors)
    ax1.set_title('📊 CO2 Kategorileri Dağılımı', fontweight='bold')
    ax1.set_xlabel('CO2 Kategorisi')
    ax1.set_ylabel('Toplam Satış')
    ax1.set_xticks(range(len(category_counts)))
    ax1.set_xticklabels(category_counts.index, rotation=45)
    
    # Değerleri göster
    for bar, value in zip(bars, category_counts.values):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(category_counts)*0.01,
                f'{value:,.0f}', ha='center', va='bottom')
    
    # 2. CO2 Dağılım Histogramı
    ax2 = axes[0, 1]
    ax2.hist(df['CO2'], bins=30, weights=df['Satış'], color='blue', alpha=0.7, edgecolor='black')
    ax2.set_title('📈 CO2 Seviyesi Dağılımı', fontweight='bold')
    ax2.set_xlabel('CO2 Seviyesi (g/km)')
    ax2.set_ylabel('Ağırlıklı Satış')
    ax2.grid(True, alpha=0.3)
    
    # Ortalama çiz
    weighted_avg = np.average(df['CO2'], weights=df['Satış'])
    ax2.axvline(weighted_avg, color='red', linestyle='--', linewidth=2,
                label=f'Ağırlıklı Ort: {weighted_avg:.1f}')
    ax2.legend()
    
    # 3. En Çok Satan Markalar
    ax3 = axes[0, 2]
    top_brands = df.groupby('Marka')['Satış'].sum().nlargest(10)
    bars = ax3.barh(range(len(top_brands)), top_brands.values, color='purple', alpha=0.7)
    ax3.set_yticks(range(len(top_brands)))
    ax3.set_yticklabels(top_brands.index)
    ax3.set_title('🏆 En Çok Satan Markalar', fontweight='bold')
    ax3.set_xlabel('Toplam Satış')
    
    # 4. Marka Bazında Ortalama CO2
    ax4 = axes[1, 0]
    brand_co2 = df.groupby('Marka').apply(lambda x: np.average(x['CO2'], weights=x['Satış']))
    top_brand_co2 = brand_co2[top_brands.index[:8]]  # En çok satan 8 marka
    bars = ax4.bar(range(len(top_brand_co2)), top_brand_co2.values, color='orange', alpha=0.7)
    ax4.set_title('🌡️ Markalara Göre Ortalama CO2', fontweight='bold')
    ax4.set_xlabel('Marka')
    ax4.set_ylabel('Ortalama CO2 (g/km)')
    ax4.set_xticks(range(len(top_brand_co2)))
    ax4.set_xticklabels(top_brand_co2.index, rotation=45, ha='right')
    
    # 5. CO2 vs Satış Scatter
    ax5 = axes[1, 1]
    scatter = ax5.scatter(df['CO2'], df['Satış'], alpha=0.6, c=df['CO2'], cmap='RdYlGn_r')
    ax5.set_title('🔗 CO2 Seviyesi vs Satış İlişkisi', fontweight='bold')
    ax5.set_xlabel('CO2 Seviyesi (g/km)')
    ax5.set_ylabel('Satış Adedi')
    ax5.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax5, label='CO2 (g/km)')
    
    # 6. Pasta Grafik
    ax6 = axes[1, 2]
    wedges, texts, autotexts = ax6.pie(category_counts.values, labels=category_counts.index,
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    ax6.set_title('🎯 CO2 Kategorileri Oranı', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('co2_emission_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # İstatistikler yazdır
    print_statistics(df)

def print_statistics(df):
    """İstatistikleri yazdır"""
    print("\n" + "="*60)
    print("📊 CO2 EMİSYON ANALİZİ - ÖZET RAPOR")
    print("="*60)
    
    print(f"\n📈 GENEL İSTATİSTİKLER:")
    print(f"🚗 Toplam Satış: {df['Satış'].sum():,.0f} araç")
    print(f"🏭 Marka Sayısı: {df['Marka'].nunique()} marka")
    print(f"🚙 Model Sayısı: {df['Model'].nunique()} model")
    
    weighted_avg = np.average(df['CO2'], weights=df['Satış'])
    print(f"\n🌡️ EMİSYON İSTATİSTİKLERİ:")
    print(f"   Ağırlıklı Ortalama CO2: {weighted_avg:.1f} g/km")
    print(f"   En Düşük CO2: {df['CO2'].min():.1f} g/km")
    print(f"   En Yüksek CO2: {df['CO2'].max():.1f} g/km")
    print(f"   Medyan CO2: {df['CO2'].median():.1f} g/km")
    
    print(f"\n🎯 CO2 KATEGORİLERİ:")
    category_stats = df.groupby('CO2_Kategori')['Satış'].sum()
    total_sales = df['Satış'].sum()
    for category, sales in category_stats.items():
        percentage = (sales / total_sales) * 100
        print(f"   {category:<15}: {sales:>10,.0f} ({percentage:>5.1f}%)")
    
    print(f"\n🏆 EN BAŞARILI MARKALAR:")
    top_brands = df.groupby('Marka')['Satış'].sum().nlargest(8)
    for i, (brand, sales) in enumerate(top_brands.items(), 1):
        market_share = (sales / total_sales) * 100
        brand_co2 = df[df['Marka'] == brand]['CO2'].mean()
        print(f"   {i}. {brand:<15}: {sales:>8,.0f} ({market_share:>4.1f}%) - {brand_co2:.0f} g/km")

def create_demo_graphs():
    """Demo grafikler oluştur"""
    print("\n🎨 Demo CO2 grafikleri oluşturuluyor...")
    
    # Demo veriler
    np.random.seed(42)
    categories = ['0-120 g/km', '121-150 g/km', '151-180 g/km', '181-200 g/km', '200+ g/km']
    sales_data = [45000, 65000, 55000, 25000, 10000]
    
    # Demo grafik
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('🚗 CO2 Emisyon Analizi (Demo)', fontsize=16, fontweight='bold')
    
    # Bar chart
    ax1 = axes[0, 0]
    colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
    bars = ax1.bar(categories, sales_data, color=colors)
    ax1.set_title('📊 CO2 Kategorileri', fontweight='bold')
    ax1.set_ylabel('Satış Adedi')
    ax1.tick_params(axis='x', rotation=45)
    
    # Pasta grafik
    ax2 = axes[0, 1]
    ax2.pie(sales_data, labels=categories, autopct='%1.1f%%', colors=colors)
    ax2.set_title('🎯 Dağılım Oranları', fontweight='bold')
    
    # Line chart
    ax3 = axes[1, 0]
    months = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz']
    trend = [15000, 18000, 22000, 20000, 25000, 23000]
    ax3.plot(months, trend, marker='o', linewidth=3, markersize=8, color='blue')
    ax3.set_title('📈 Aylık Trend', fontweight='bold')
    ax3.set_ylabel('Satış Adedi')
    ax3.grid(True, alpha=0.3)
    
    # Histogram
    ax4 = axes[1, 1]
    co2_values = np.random.normal(145, 25, 1000)
    ax4.hist(co2_values, bins=30, color='purple', alpha=0.7, edgecolor='black')
    ax4.set_title('📈 CO2 Dağılımı', fontweight='bold')
    ax4.set_xlabel('CO2 (g/km)')
    ax4.set_ylabel('Frekans')
    
    plt.tight_layout()
    plt.savefig('co2_demo_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n📊 DEMO RAPOR:")
    print("="*40)
    print("📅 2021 yılı için demo analiz")
    print(f"🚗 Toplam: {sum(sales_data):,} araç")
    print("✅ Grafikler başarıyla oluşturuldu!")

if __name__ == "__main__":
    main()