# 🚗 Türkiye Otomotiv CO2 Emisyon Analizi - Sonuçlar

Bu klasör, 2021 yılı Türkiye otomotiv pazarı CO2 emisyon analizi çalışmasının tüm sonuçlarını içermektedir.

## 📁 Klasör Yapısı

### 📊 **grafikler/**
- `co2_emission_analysis.png` - Ana CO2 emisyon analiz grafikleri (6 farklı grafik)

### 📄 **raporlar/**
- `CO2_Emisyon_Analiz_Raporu.md` - Türkçe detaylı analiz raporu
- `brands_models_generations_analizi.md` - Marka model jenerasyon analizi

### 🎓 **akademik/**
- `CO2_Emissions_Analysis_Turkish_Automotive_Market_2021.md` - İngilizce akademik makale

### 💾 **veri/**
- `Marka_Model_Emisyon Bilgisi_2021_2024.xls` - Ana veri seti (2.0MB)
- `emission_dataset.xlsx` - İşlenmiş veri (674 satır)
- `emission_dataset_revised.xlsx` - Revize edilmiş veri (408 satır)

### 🐍 **kodlar/**
- `simple_co2_analysis.py` - Basit CO2 analizi
- `comprehensive_co2_analysis.py` - Kapsamlı analiz scripti
- `co2_emission_analysis.py` - Ana analiz kodu
- `dataset_rearrange.py` - Veri düzenleme scripti
- `fuller_test.py` - İstatistiksel test scripti
- `requirements.txt` - Gerekli Python paketleri

## 🎯 Ana Bulgular

### 📈 **Genel İstatistikler:**
- **Toplam Analiz Edilen Araç:** 919,156
- **Marka Sayısı:** 39
- **Model Sayısı:** 237
- **Ağırlıklı Ortalama CO2:** 133.7 g/km

### 🏆 **En Çevre Dostu Markalar:**
1. **Toyota** - 103 g/km 🥇
2. **Peugeot** - 109 g/km 🥈
3. **Renault** - 113 g/km 🥉

### 📊 **CO2 Kategori Dağılımı:**
- 🟢 **Mükemmel (0-120 g/km):** %39.7
- 🟡 **İyi (121-150 g/km):** %43.2
- 🟠 **Orta (151-180 g/km):** %9.9
- 🔴 **Yüksek (180+ g/km):** %7.2

### ✅ **Çevresel Performans:**
- **%82.9** araç AB standartlarını karşılıyor (<150 g/km)
- Küresel ortalamadan **%8.6** daha iyi performans
- AB ortalamasından **%13.1** yüksek

## 🔧 Kullanım

### Python Kodlarını Çalıştırmak için:
```bash
pip install -r kodlar/requirements.txt
python kodlar/simple_co2_analysis.py
```

### Grafikleri Görüntülemek için:
- `grafikler/co2_emission_analysis.png` dosyasını açın

### Raporları Okumak için:
- Türkçe: `raporlar/CO2_Emisyon_Analiz_Raporu.md`
- İngilizce Akademik: `akademik/CO2_Emissions_Analysis_Turkish_Automotive_Market_2021.md`

## 📚 Akademik Yayın

İngilizce akademik makale aşağıdaki dergilere gönderilebilir:
- Transportation Research Part D: Transport and Environment
- Journal of Cleaner Production
- Energy Policy
- Sustainability

## 📧 İletişim

Bu analiz çalışması hakkında sorularınız için GitHub issues bölümünü kullanabilirsiniz.

---
**Oluşturulma Tarihi:** 2024
**Analiz Dönemi:** 2021 Yılı
**Veri Kaynağı:** Marka Model Emisyon Bilgisi 2021-2024