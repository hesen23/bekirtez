import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Load emission and brand data"""
    try:
        # Load emission data
        emission_df = pd.read_excel('data/emission_dataset.xlsx', sheet_name=None)
        
        # Load brand-model data
        brands_models_df = pd.read_excel('brands_models_generations.xlsx')
        
        # Load brands list
        brands_df = pd.read_excel('brands.xlsx')
        
        return emission_df, brands_models_df, brands_df
    except Exception as e:
        print(f"Veri yükleme hatası: {e}")
        return None, None, None

def create_brand_distribution_chart(brands_models_df):
    """Top markalar dağılım grafiği"""
    plt.figure(figsize=(14, 8))
    
    # Top 15 marka
    brand_counts = brands_models_df['Marka'].value_counts().head(15)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(brand_counts)))
    bars = plt.bar(range(len(brand_counts)), brand_counts.values, color=colors)
    
    plt.title('Top 15 Marka - Veri Kayıt Sayısı Dağılımı\n2021-2024 Dönemi', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Markalar', fontsize=12, fontweight='bold')
    plt.ylabel('Kayıt Sayısı', fontsize=12, fontweight='bold')
    
    # X-axis labels
    plt.xticks(range(len(brand_counts)), brand_counts.index, 
               rotation=45, ha='right', fontsize=10)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('brand_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_emission_performance_chart():
    """Emisyon performansı karşılaştırma grafiği"""
    plt.figure(figsize=(14, 8))
    
    # Örnek emisyon verileri (makaleden)
    brands = ['Tesla', 'Toyota', 'BMW', 'Mercedes-Benz', 'Audi', 
              'Hyundai', 'Kia', 'Volkswagen', 'Ford', 'Renault']
    emissions = [0, 118, 142, 145, 148, 135, 138, 144, 149, 152]
    categories = ['Elektrikli', 'Hibrit', 'Premium', 'Premium', 'Premium',
                  'Mainstream', 'Mainstream', 'Premium', 'Mainstream', 'Mainstream']
    
    # Color mapping
    color_map = {'Elektrikli': '#2E8B57', 'Hibrit': '#4682B4', 
                 'Premium': '#DC143C', 'Mainstream': '#FF8C00'}
    colors = [color_map[cat] for cat in categories]
    
    bars = plt.bar(brands, emissions, color=colors, alpha=0.8)
    
    plt.title('Marka Bazında CO₂ Emisyon Performansı\n(g/km)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Markalar', fontsize=12, fontweight='bold')
    plt.ylabel('CO₂ Emisyonu (g/km)', fontsize=12, fontweight='bold')
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        if height == 0:
            plt.text(bar.get_x() + bar.get_width()/2., height + 3,
                    '0\n(Elektrikli)', ha='center', va='bottom', 
                    fontweight='bold', fontsize=9)
        else:
            plt.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color_map[cat], label=cat) 
                      for cat in color_map.keys()]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('emission_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_technology_trend_chart():
    """Teknoloji dağılımı ve trend grafiği"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # 2024 Teknoloji dağılımı (Pie Chart)
    technologies = ['Geleneksel ICE', 'Hibrit (HEV)', 'Plug-in Hibrit (PHEV)', 'Tam Elektrikli (BEV)']
    percentages = [68, 18, 9, 5]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    wedges, texts, autotexts = ax1.pie(percentages, labels=technologies, autopct='%1.1f%%',
                                       colors=colors, startangle=90)
    ax1.set_title('2024 Motor Teknolojisi Dağılımı', fontsize=14, fontweight='bold')
    
    # Trend Chart (2021-2024)
    years = [2021, 2022, 2023, 2024]
    ice_trend = [82, 76, 72, 68]
    hybrid_trend = [8.4, 12, 15, 18]
    phev_trend = [5, 6.5, 7.5, 9]
    bev_trend = [1.2, 2.5, 3.8, 5]
    
    ax2.plot(years, ice_trend, marker='o', linewidth=3, label='Geleneksel ICE', color='#FF6B6B')
    ax2.plot(years, hybrid_trend, marker='s', linewidth=3, label='Hibrit (HEV)', color='#4ECDC4')
    ax2.plot(years, phev_trend, marker='^', linewidth=3, label='Plug-in Hibrit', color='#45B7D1')
    ax2.plot(years, bev_trend, marker='D', linewidth=3, label='Tam Elektrikli', color='#96CEB4')
    
    ax2.set_title('Teknoloji Trendleri (2021-2024)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Yıl', fontweight='bold')
    ax2.set_ylabel('Pazar Payı (%)', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('technology_trends.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_model_complexity_chart(brands_models_df):
    """En çok varyasyona sahip modeller"""
    plt.figure(figsize=(14, 10))
    
    # Model bazında versiyon sayıları
    model_versions = brands_models_df.groupby(['Marka', 'Model']).size().reset_index(name='Versiyon_Sayisi')
    top_models = model_versions.nlargest(10, 'Versiyon_Sayisi')
    
    # Model adlarını oluştur
    model_labels = [f"{row['Marka']}\n{row['Model']}" for _, row in top_models.iterrows()]
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_models)))
    bars = plt.barh(range(len(top_models)), top_models['Versiyon_Sayisi'], color=colors)
    
    plt.title('En Çok Varyasyona Sahip Top 10 Model\n(Alt Versiyon Sayısı)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Versiyon Sayısı', fontsize=12, fontweight='bold')
    plt.ylabel('Modeller', fontsize=12, fontweight='bold')
    
    plt.yticks(range(len(top_models)), model_labels, fontsize=10)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 10, bar.get_y() + bar.get_height()/2,
                f'{int(width)}', ha='left', va='center', fontweight='bold')
    
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('model_complexity.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_yearly_emission_trend():
    """Yıllık emisyon trendi"""
    plt.figure(figsize=(12, 8))
    
    years = [2021, 2022, 2023, 2024]
    avg_emissions = [158, 148, 138, 128]
    electric_share = [1.2, 2.5, 3.8, 5.2]
    
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Emisyon trendi (sol y-axis)
    color = '#E74C3C'
    ax1.set_xlabel('Yıl', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Ortalama CO₂ Emisyonu (g/km)', color=color, fontsize=12, fontweight='bold')
    line1 = ax1.plot(years, avg_emissions, color=color, marker='o', linewidth=4, 
                     markersize=8, label='Ortalama Emisyon')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Elektrikli araç payı (sağ y-axis)
    ax2 = ax1.twinx()
    color = '#27AE60'
    ax2.set_ylabel('Elektrikli Araç Payı (%)', color=color, fontsize=12, fontweight='bold')
    line2 = ax2.plot(years, electric_share, color=color, marker='s', linewidth=4, 
                     markersize=8, label='Elektrikli Araç Payı')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Values on points
    for i, (year, emission, electric) in enumerate(zip(years, avg_emissions, electric_share)):
        ax1.annotate(f'{emission}g/km', (year, emission), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontweight='bold')
        ax2.annotate(f'{electric}%', (year, electric), textcoords="offset points", 
                    xytext=(0,-15), ha='center', fontweight='bold', color='#27AE60')
    
    plt.title('Türkiye Otomotiv Sektörü: Emisyon Azalışı ve Elektrikli Araç Artışı\n2021-2024 Dönemi', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right')
    
    plt.tight_layout()
    plt.savefig('yearly_emission_trend.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_segment_analysis():
    """Segment analizi grafiği"""
    plt.figure(figsize=(14, 10))
    
    # Segment verileri
    segments = ['Compact', 'Executive', 'Luxury', 'SUV', 'Ticari', 'Sports']
    brands_count = [12, 8, 5, 15, 6, 4]
    avg_emissions = [135, 155, 180, 165, 190, 200]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    # Segment bazında marka sayısı
    colors1 = plt.cm.Set2(np.linspace(0, 1, len(segments)))
    bars1 = ax1.bar(segments, brands_count, color=colors1, alpha=0.8)
    ax1.set_title('Segment Bazında Marka Çeşitliliği', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Marka Sayısı', fontweight='bold')
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Segment bazında ortalama emisyon
    colors2 = plt.cm.Reds(np.linspace(0.3, 0.9, len(segments)))
    bars2 = ax2.bar(segments, avg_emissions, color=colors2, alpha=0.8)
    ax2.set_title('Segment Bazında Ortalama CO₂ Emisyonu', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Araç Segmentleri', fontweight='bold')
    ax2.set_ylabel('Ortalama CO₂ (g/km)', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('segment_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_statistical_summary():
    """İstatistiksel özet dashboard"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Marka dağılımı (Top 10)
    brands = ['Volkswagen', 'Mercedes-Benz', 'Ford', 'Audi', 'BMW', 
              'Toyota', 'Opel', 'Renault', 'Citroën', 'Nissan']
    values = [3867, 3787, 3407, 3015, 2897, 2429, 2304, 2022, 1484, 1452]
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(brands)))
    bars = ax1.barh(brands, values, color=colors)
    ax1.set_title('Top 10 Marka - Kayıt Sayısı', fontweight='bold')
    ax1.set_xlabel('Kayıt Sayısı')
    
    # 2. Teknoloji dağılımı
    techs = ['ICE', 'HEV', 'PHEV', 'BEV']
    tech_values = [68, 18, 9, 5]
    ax2.pie(tech_values, labels=techs, autopct='%1.1f%%', startangle=90,
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax2.set_title('2024 Teknoloji Dağılımı (%)', fontweight='bold')
    
    # 3. Yıllık trend
    years = [2021, 2022, 2023, 2024]
    emissions = [158, 148, 138, 128]
    ax3.plot(years, emissions, marker='o', linewidth=3, markersize=8, color='#E74C3C')
    ax3.set_title('Ortalama Emisyon Trendi', fontweight='bold')
    ax3.set_ylabel('CO₂ (g/km)')
    ax3.grid(True, alpha=0.3)
    
    # 4. En popüler modeller
    models = ['BMW 3 Serisi', 'Mercedes E-Serisi', 'VW Golf', 'Mercedes C-Serisi', 'Audi A4']
    model_versions = [828, 720, 683, 643, 554]
    ax4.bar(range(len(models)), model_versions, color='#3498DB')
    ax4.set_title('En Çok Varyasyona Sahip Modeller', fontweight='bold')
    ax4.set_ylabel('Versiyon Sayısı')
    ax4.set_xticks(range(len(models)))
    ax4.set_xticklabels(models, rotation=45, ha='right')
    
    plt.suptitle('Türkiye Otomotiv Emisyon Analizi - Özet Dashboard\n2021-2024 Dönemi', 
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('statistical_summary_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Ana fonksiyon - tüm grafikleri oluştur"""
    print("🎨 Emisyon Verisi Görselleştirmeleri Oluşturuluyor...")
    print("=" * 50)
    
    # Veri yükleme
    emission_df, brands_models_df, brands_df = load_data()
    
    if brands_models_df is not None:
        print("✅ Veriler başarıyla yüklendi")
        
        print("\n📊 Grafik 1: Marka Dağılımı")
        create_brand_distribution_chart(brands_models_df)
        
        print("\n📊 Grafik 2: Emisyon Performansı")
        create_emission_performance_chart()
        
        print("\n📊 Grafik 3: Teknoloji Trendleri")
        create_technology_trend_chart()
        
        print("\n📊 Grafik 4: Model Karmaşıklığı")
        create_model_complexity_chart(brands_models_df)
        
        print("\n📊 Grafik 5: Yıllık Emisyon Trendi")
        create_yearly_emission_trend()
        
        print("\n📊 Grafik 6: Segment Analizi")
        create_segment_analysis()
        
        print("\n📊 Grafik 7: İstatistiksel Özet Dashboard")
        create_statistical_summary()
        
        print("\n✅ Tüm grafikler başarıyla oluşturuldu!")
        print("📁 Grafikler workspace klasörüne PNG formatında kaydedildi")
        
    else:
        print("❌ Veri yüklenemedi, örnek grafikler oluşturuluyor...")
        create_emission_performance_chart()
        create_technology_trend_chart()
        create_yearly_emission_trend()
        create_segment_analysis()
        create_statistical_summary()

if __name__ == "__main__":
    main()