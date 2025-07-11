import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği için
plt.rcParams['font.family'] = ['DejaVu Sans']

def analyze_co2_emissions():
    print("🚗 CO2 Emisyon Analizi Başlatılıyor...")
    
    # Ana emisyon dosyasını okuma denemesi
    try:
        print("📂 Ana emisyon dosyası okunuyor...")
        df_main = pd.read_excel('Marka_Model_Emisyon Bilgisi_2021_2024.xls', sheet_name=None)
        print(f"✅ Ana dosya başarıyla okundu! Sayfa sayısı: {len(df_main.keys())}")
        
        # Sayfaları listele
        print("\n📋 Bulunan sayfalar:")
        for i, sheet_name in enumerate(df_main.keys(), 1):
            print(f"{i}. {sheet_name} - Boyut: {df_main[sheet_name].shape}")
            
        # İlk sayfanın sütunlarını göster
        first_sheet = list(df_main.keys())[0]
        print(f"\n🔍 '{first_sheet}' sayfasının sütunları:")
        print(df_main[first_sheet].columns.tolist())
        print(f"\nİlk 3 satır:")
        print(df_main[first_sheet].head(3))
        
        # CO2 emisyon verilerini ara
        co2_data = None
        co2_sheet = None
        
        for sheet_name, sheet_df in df_main.items():
            # CO2 ile ilgili sütunları ara
            co2_columns = [col for col in sheet_df.columns if 'co2' in str(col).lower() or 'emisyon' in str(col).lower()]
            if co2_columns:
                print(f"\n🎯 '{sheet_name}' sayfasında CO2 sütunları bulundu: {co2_columns}")
                co2_data = sheet_df
                co2_sheet = sheet_name
                break
        
        if co2_data is None:
            print("⚠️ Ana dosyada CO2 verisi bulunamadı, işlenmiş veriyi kontrol ediyorum...")
            
            # İşlenmiş veriyi kontrol et
            if os.path.exists('data/emission_dataset_revised.xlsx'):
                df_revised = pd.read_excel('data/emission_dataset_revised.xlsx', sheet_name=None)
                print(f"📊 İşlenmiş veri okundu! Sayfa sayısı: {len(df_revised.keys())}")
                
                # ek7 sayfasını kontrol et (Emisyon değerleri)
                if 'ek7' in df_revised:
                    co2_data = df_revised['ek7']
                    co2_sheet = 'ek7'
                    print("✅ Emisyon değerleri (ek7) sayfası bulundu!")
            
            if co2_data is None:
                # Alternatif olarak data/emission_dataset.xlsx'i dene
                df_original = pd.read_excel('data/emission_dataset.xlsx', sheet_name=None)
                print(f"📈 Orijinal işlenmiş veri okundu! Sayfa sayısı: {len(df_original.keys())}")
                
                for sheet_name in df_original.keys():
                    print(f"   - {sheet_name}: {df_original[sheet_name].shape}")
                
                # ek7 sayfasını kontrol et
                if 'ek7' in df_original:
                    co2_data = df_original['ek7']
                    co2_sheet = 'ek7'
                    print("✅ ek7 (Emisyon değerleri) sayfası bulundu!")
        
        if co2_data is not None:
            create_co2_visualizations(co2_data, co2_sheet)
        else:
            print("❌ CO2 emisyon verileri bulunamadı!")
            
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        print("🔄 Alternatif veri kaynaklarını deniyorum...")
        
        # Alternatif dosyaları dene
        try_alternative_sources()

def try_alternative_sources():
    """Alternatif veri kaynaklarını dene"""
    try:
        # İşlenmiş veriyi dene
        if os.path.exists('data/emission_dataset.xlsx'):
            print("📊 İşlenmiş emisyon verisini okuyorum...")
            df = pd.read_excel('data/emission_dataset.xlsx', sheet_name=None)
            
            print("🔍 Bulunan sayfalar:")
            for sheet_name in df.keys():
                print(f"   - {sheet_name}: {df[sheet_name].shape}")
                if 'ek7' in sheet_name.lower() or 'emisyon' in sheet_name.lower():
                    print(f"     🎯 Bu sayfa emisyon verileri içerebilir")
                    print(f"     Sütunlar: {df[sheet_name].columns.tolist()}")
            
            # ek7 sayfasını kullan
            if 'ek7' in df:
                create_co2_visualizations(df['ek7'], 'ek7')
            else:
                # İlk sayfa ile devam et
                first_sheet = list(df.keys())[0]
                create_sample_visualization(df[first_sheet], first_sheet)
                
    except Exception as e:
        print(f"❌ Alternatif kaynak hatası: {str(e)}")
        # Sample data ile demo oluştur
        create_demo_visualization()

def create_co2_visualizations(data, sheet_name):
    """CO2 emisyon verilerini görselleştir"""
    print(f"\n📊 '{sheet_name}' verisi ile grafik oluşturuluyor...")
    print(f"Veri boyutu: {data.shape}")
    print(f"Sütunlar: {data.columns.tolist()}")
    
    # Veriyi temizle
    df = data.copy()
    
    # Tarih sütunları var mı kontrol et
    date_columns = []
    for col in df.columns:
        if any(keyword in str(col).lower() for keyword in ['yıl', 'year', 'ay', 'month', 'tarih', 'date']):
            date_columns.append(col)
    
    print(f"📅 Tarih sütunları: {date_columns}")
    
    # Sayısal sütunları bul
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"🔢 Sayısal sütunlar: {numeric_cols}")
    
    # Grafik oluştur
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'🚗 CO2 Emisyon Analizi - {sheet_name.upper()}', fontsize=16, fontweight='bold')
    
    # 1. Zaman serisi analizi (eğer tarih verileri varsa)
    if len(date_columns) >= 1 and len(numeric_cols) > 0:
        ax1 = axes[0, 0]
        
        # Yıl ve ay sütunları varsa birleştir
        if 'Yıl' in df.columns and 'Ay' in df.columns:
            df['Tarih'] = pd.to_datetime(df[['Yıl', 'Ay']].assign(Day=1))
            
            # En yüksek değerli sütunları seç
            value_col = numeric_cols[0] if numeric_cols else None
            if value_col:
                monthly_data = df.groupby('Tarih')[value_col].sum().reset_index()
                ax1.plot(monthly_data['Tarih'], monthly_data[value_col], marker='o', linewidth=2)
                ax1.set_title('📈 Aylık Emisyon Trendi', fontweight='bold')
                ax1.set_xlabel('Tarih')
                ax1.set_ylabel('Emisyon Değeri')
                ax1.grid(True, alpha=0.3)
                ax1.tick_params(axis='x', rotation=45)
    else:
        ax1 = axes[0, 0]
        ax1.text(0.5, 0.5, 'Zaman Serisi Verisi\nBulunamadı', ha='center', va='center', fontsize=12)
        ax1.set_title('📈 Zaman Serisi Analizi')
    
    # 2. En yüksek emisyon değerleri (Top 10)
    ax2 = axes[0, 1]
    if len(numeric_cols) > 0:
        # En yüksek toplamı olan sütunları bul
        top_columns = []
        for col in numeric_cols:
            if df[col].sum() > 0:
                top_columns.append((col, df[col].sum()))
        
        if top_columns:
            top_columns = sorted(top_columns, key=lambda x: x[1], reverse=True)[:10]
            categories = [item[0] for item in top_columns]
            values = [item[1] for item in top_columns]
            
            bars = ax2.bar(range(len(categories)), values, color='red', alpha=0.7)
            ax2.set_title('🔝 En Yüksek Emisyon Kategorileri', fontweight='bold')
            ax2.set_xlabel('Kategori')
            ax2.set_ylabel('Toplam Emisyon')
            ax2.set_xticks(range(len(categories)))
            ax2.set_xticklabels(categories, rotation=45, ha='right')
            
            # Değerleri barların üstüne yaz
            for bar, value in zip(bars, values):
                ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(values)*0.01,
                        f'{value:,.0f}', ha='center', va='bottom', fontsize=8)
    else:
        ax2.text(0.5, 0.5, 'Sayısal Emisyon\nVerisi Bulunamadı', ha='center', va='center', fontsize=12)
        ax2.set_title('🔝 En Yüksek Emisyon Kategorileri')
    
    # 3. Yıllık karşılaştırma
    ax3 = axes[1, 0]
    if 'Yıl' in df.columns and len(numeric_cols) > 0:
        yearly_data = df.groupby('Yıl')[numeric_cols].sum()
        total_by_year = yearly_data.sum(axis=1)
        
        bars = ax3.bar(total_by_year.index, total_by_year.values, 
                      color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'][:len(total_by_year)])
        ax3.set_title('📊 Yıllık Toplam Emisyon', fontweight='bold')
        ax3.set_xlabel('Yıl')
        ax3.set_ylabel('Toplam Emisyon')
        
        # Değerleri barların üstüne yaz
        for bar, value in zip(bars, total_by_year.values):
            ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(total_by_year)*0.01,
                    f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'Yıllık Karşılaştırma\nVerisi Bulunamadı', ha='center', va='center', fontsize=12)
        ax3.set_title('📊 Yıllık Karşılaştırma')
    
    # 4. Dağılım analizi
    ax4 = axes[1, 1]
    if len(numeric_cols) > 0:
        # İlk sayısal sütunun dağılımını göster
        main_col = numeric_cols[0]
        non_zero_data = df[df[main_col] > 0][main_col]
        
        if len(non_zero_data) > 0:
            ax4.hist(non_zero_data, bins=30, color='green', alpha=0.7, edgecolor='black')
            ax4.set_title(f'📈 {main_col} Dağılımı', fontweight='bold')
            ax4.set_xlabel('Emisyon Değeri')
            ax4.set_ylabel('Frekans')
            ax4.grid(True, alpha=0.3)
            
            # İstatistikler ekle
            mean_val = non_zero_data.mean()
            median_val = non_zero_data.median()
            ax4.axvline(mean_val, color='red', linestyle='--', label=f'Ortalama: {mean_val:.1f}')
            ax4.axvline(median_val, color='orange', linestyle='--', label=f'Medyan: {median_val:.1f}')
            ax4.legend()
    else:
        ax4.text(0.5, 0.5, 'Dağılım Analizi\nİçin Veri Yok', ha='center', va='center', fontsize=12)
        ax4.set_title('📈 Emisyon Dağılımı')
    
    plt.tight_layout()
    plt.savefig('co2_emission_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Özet istatistikler
    print("\n📈 ÖZET İSTATİSTİKLER:")
    print("="*50)
    if len(numeric_cols) > 0:
        for col in numeric_cols[:5]:  # İlk 5 sayısal sütun
            total = df[col].sum()
            mean = df[col].mean()
            if total > 0:
                print(f"{col:<30}: Toplam={total:>10,.0f}, Ortalama={mean:>8.1f}")

def create_demo_visualization():
    """Demo CO2 emisyon grafiği oluştur"""
    print("\n🎨 Demo CO2 emisyon grafiği oluşturuluyor...")
    
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
    plt.style.use('seaborn-v0_8')
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
    import os
    analyze_co2_emissions()