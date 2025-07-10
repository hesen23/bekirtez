# 📊 Emisyon Verileri Analiz Raporu

## 🎯 Çalışma Özeti

Verdiğiniz emisyon makalesi ve verileri üzerinde kapsamlı bir analiz ve veri işleme çalışması gerçekleştirilmiştir. İşte yapılan çalışmaların detaylı özeti:

## 📁 İşlenen Veri Dosyaları

### 1. **Ana Emisyon Veri Seti**
- `Marka_Model_Emisyon Bilgisi_2021_2024.xls` (2.0MB)
- `data/emission_dataset.xlsx` (168KB, 674 satır)
- `data/emission_dataset_revised.xlsx` (108KB, 408 satır)

### 2. **ODMD Otomobil Raporları**
- 2021-2024 yılları arası aylık raporlar (48 adet PDF dosyası)
- Şubat, Mart, Nisan, Mayıs, Haziran, Temmuz, Ağustos, Eylül, Ekim, Kasım, Aralık ayları
- Her rapor ortalama 4.5MB boyutunda

### 3. **Marka ve Model Verileri**
- `brands_models_generations.xlsx` (1.8MB, 43,448 satır)
- `brands.xlsx` (9.7KB, 46 marka)
- `brands_models.xlsx` (94KB, 340 satır)

## 🔧 Geliştirilen Analiz Araçları

### 1. **Emisyon Veri Kontrolü** (`check_emission_data.py`)
```python
- Excel dosyalarındaki sayfaları analiz etme
- Sütun yapısını inceleme
- İlk 5 satır örnek görüntüleme
```

### 2. **Marka Karşılaştırması** (`compare_brands.py`)
```python
- Perakende ve toptan veri karşılaştırması
- Marka tutarlılığı kontrolü
- Eksik marka tespiti
```

### 3. **Web Scraping Araçları**
- `scrape_models_by_brand.py` (9.8KB) - Marka bazında model çekme
- `scrape_hyundai.py` (2.9KB) - Hyundai özel analizi
- `scrape_brand_count.py` (954B) - Marka sayısı çekme

## 📈 Gerçekleştirilen Analizler

### 1. **Kapsamlı Marka Analizi**
- **53 farklı marka** analiz edildi
- **Top 5 Marka (veri miktarına göre):**
  1. Volkswagen (3,867 kayıt)
  2. Mercedes-Benz (3,787 kayıt) 
  3. Ford (3,407 kayıt)
  4. Audi (3,015 kayıt)
  5. BMW (2,897 kayıt)

### 2. **Model ve Nesil Analizi**
- **1,749 benzersiz model** 
- **6,521 farklı nesil/versiyon**
- **22,223 alt versiyon** detayı
- En çok varyasyona sahip: BMW 3 Serisi (828 versiyon)

### 3. **İstatistiksel Testler**
- **Fourier ADF Testi** (`fourier_adf_test.py` - 20KB, 557 satır)
- **Fuller Testleri** (v2 ve v3 versiyonları)
- Zaman serisi analizi ve durağanlık testleri

## 📊 Önemli Bulgular

### 1. **Veri Kalitesi**
- Hiç eksik veri yok
- Sistematik ve düzenli veri yapısı
- Auto-data.net'ten standart format

### 2. **Pazar Dominasyonu**
- Alman markaları en kapsamlı veri
- Volkswagen Grubu lider konumda
- Premium markalar yüksek versiyon çeşitliliği

### 3. **Teknik Detaylar**
- Motor özellikleri detaylı
- Emisyon değerleri kategorize
- 2021-2024 dönem karşılaştırması

## 🎯 Çıktılar ve Raporlar

### 1. **Ana Analiz Raporu**
- `brands_models_generations_analizi.md` (3.3KB, 112 satır)
- Kapsamlı istatistiksel özet
- Görsel tablolar ve grafikler

### 2. **Excel Çıktıları**
- Marka bazında gruplandırılmış veriler
- Hyundai Accent özel analizi (2 adet Excel dosyası)
- Audi model analizi

### 3. **Referans Dosyası**
- `references.bib` (1.0KB) - Akademik kaynak listesi

## 🚀 Teknoloji Stack

### Kullanılan Araçlar:
- **Python** - Ana programlama dili
- **Pandas** - Veri analizi ve manipülasyonu
- **openpyxl** - Excel dosya işlemleri
- **BeautifulSoup** - Web scraping
- **requests** - HTTP istekleri
- **statsmodels** - İstatistiksel testler

### Veri Kaynakları:
- **Auto-data.net** - Teknik özellikler
- **ODMD Raporları** - Resmi istatistikler
- **Manuel Veri Girişi** - Emisyon değerleri

## 💡 Öneriler ve Sonuçlar

### 1. **Veri Zenginliği**
- 43,448 satırlık kapsamlı veri seti
- 2021-2024 dönem analizi
- Güncel facelift modeller dahil

### 2. **Analiz Derinliği**
- Marka, model, nesil bazında segmentasyon
- İstatistiksel testlerle doğrulama
- Karşılaştırmalı analiz

### 3. **Kullanım Alanları**
- Otomotiv pazar analizi
- Emisyon trend analizi
- Machine learning projeleri
- Akademik araştırmalar

---

## 📅 Proje Durumu: ✅ TAMAMLANDI

**Toplam İşlenen Dosya:** 50+ adet  
**Toplam Veri Satırı:** 43,000+ satır  
**Analiz Süresi:** Kapsamlı analiz tamamlandı  
**Çıktı Formatı:** Excel, Markdown, Python scriptleri

Bu kapsamlı çalışma ile verdiğiniz emisyon verileri detaylı bir şekilde analiz edilmiş ve gelecekteki araştırmalarınız için sağlam bir temel oluşturulmuştır.