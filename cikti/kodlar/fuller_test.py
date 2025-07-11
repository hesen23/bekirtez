import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import glob

def perform_fuller_test(data, column_name):
    """
    Fuller (Dickey-Fuller) durağanlık testi uygular
    
    Parameters:
    -----------
    data : pandas.Series
        Test edilecek zaman serisi
    column_name : str
        Değişken adı
    
    Returns:
    --------
    dict
        Test sonuçları
    """
    print(f"Test ediliyor: {column_name}")
    result = adfuller(data.dropna())
    
    return {
        'Değişken': column_name.replace('_', ' '),
        'ADF İstatistiği': result[0],
        'p-değeri': result[1],
        'Kritik Değerler': result[4],
        'Gözlem Sayısı': result[3],
        'Sonuç': 'Durağan' if result[1] < 0.05 else 'Durağan Değil'
    }

def create_latex_table(results, sheet_name):
    """
    LaTeX tablosu oluşturur
    
    Parameters:
    -----------
    results : list
        Test sonuçları listesi
    sheet_name : str
        Çalışma sayfası adı
    
    Returns:
    --------
    str
        LaTeX tablosu
    """
    latex_table = f"""\\begin{{table}}[H]
\\centering
\\caption{{Fuller (Dickey-Fuller) Durağanlık Testi Sonuçları - {sheet_name}}}
\\label{{tab:fuller_test_{sheet_name}}}
\\begin{{threeparttable}}
\\begin{{tabular}}{{lS[table-format=-2.4]S[table-format=1.4]S[table-format=-2.4]S[table-format=-2.4]l}}
\\toprule
Değişken & {{ADF İstatistiği}} & {{p-değeri}} & {{1\\%}} & {{5\\%}} & {{Sonuç}} \\\\
\\midrule
"""
    
    for result in results:
        latex_table += f"{result['Değişken']} & {result['ADF İstatistiği']:.4f} & {result['p-değeri']:.4f} & "
        latex_table += f"{result['Kritik Değerler']['1%']:.4f} & {result['Kritik Değerler']['5%']:.4f} & "
        latex_table += f"{result['Sonuç']} \\\\\n"
    
    latex_table += """\\bottomrule
\\end{tabular}
\\begin{tablenotes}
\\small
\\item[1] H0: Seri durağan değil
\\item[2] H1: Seri durağan
\\item[3] Kritik değerler: MacKinnon (1996) tablolarından alınmıştır
\\end{tablenotes}
\\end{threeparttable}
\\end{table}
"""
    
    return latex_table

def create_info_text():
    """
    Durağanlık testi hakkında detaylı bilgi metni oluşturur
    
    Returns:
    --------
    str
        Bilgi metni
    """
    info_text = """\\section{Fuller (Dickey-Fuller) Durağanlık Testi Hakkında}

Fuller (Dickey-Fuller) durağanlık testi, zaman serisi verilerinin durağan olup olmadığını belirlemek için kullanılan bir istatistiksel testtir. Bu test, seride birim kök varlığını araştırır.

\\subsection{Test Formülü}

Basit bir AR(1) modeli için Fuller testi denklemi:

\\[
\\Delta y_t = \\alpha + \\beta t + \\gamma y_{t-1} + \\varepsilon_t
\\]

Burada:
\\begin{itemize}
    \\item $\\Delta y_t$: Serinin birinci farkı
    \\item $\\alpha$: Sabit terim
    \\item $\\beta t$: Trend terimi
    \\item $\\gamma$: Test edilecek parametre
    \\item $\\varepsilon_t$: Hata terimi
\\end{itemize}

\\subsection{Hipotezler}

\\begin{itemize}
    \\item $H_0: \\gamma = 0$ (Seri durağan değil, birim kök içerir)
    \\item $H_1: \\gamma < 0$ (Seri durağandır)
\\end{itemize}

\\subsection{Test Sonuçlarının Detaylı Yorumlanması}

\\begin{itemize}
    \\item \\textbf{ADF İstatistiği:} Test istatistiği. Bu değer, kritik değerlerle karşılaştırılır. Eğer ADF istatistiği kritik değerlerden daha küçükse (daha negatifse), null hipotezi reddedilir ve seri durağan kabul edilir.
    
    \\item \\textbf{p-değeri:} Bu değer, null hipotezinin reddedilme olasılığını gösterir. Genellikle 0.05 eşik değeri kullanılır:
    \\begin{itemize}
        \\item p-değeri < 0.05 ise, null hipotezi reddedilir ve seri durağan kabul edilir.
        \\item p-değeri > 0.05 ise, null hipotezi reddedilemez ve seri durağan değil kabul edilir.
    \\end{itemize}
    
    \\item \\textbf{Kritik Değerler:} Farklı anlamlılık düzeyleri (genellikle \\%1, \\%5 ve \\%10) için eşik değerlerdir. ADF istatistiği bu değerlerden küçükse, ilgili anlamlılık düzeyinde seri durağan kabul edilir.
    
    \\item \\textbf{Gözlem Sayısı:} Analizde kullanılan veri noktalarının sayısı. Daha fazla gözlem, genellikle daha güvenilir sonuçlar verir.
    
    \\item \\textbf{Sonuç:} "Durağan" veya "Durağan Değil" şeklinde özetlenir. Bu sonuç, p-değerine dayanarak belirlenir.
\\end{itemize}

\\subsection{Sonuçların Pratik Yorumlanması}

\\begin{itemize}
    \\item \\textbf{Durağan Seri:} Zaman içinde sabit bir ortalama, varyans ve otokorelasyon yapısına sahiptir. Bu tür seriler, tahmin ve modelleme için daha uygundur.
    
    \\item \\textbf{Durağan Olmayan Seri:} Zaman içinde değişen istatistiksel özelliklere sahiptir. Bu tür seriler, yanıltıcı regresyonlara ve hatalı tahminlere yol açabilir.
    
    \\item \\textbf{Fark Alma:} Durağan olmayan seriler genellikle fark alınarak durağan hale getirilebilir. Birinci dereceden fark alma işlemi: $\\Delta y_t = y_t - y_{t-1}$
    
    \\item \\textbf{Trend Durağanlık:} Bazı seriler, trend etkisi kaldırıldığında durağan hale gelebilir. Bu durumda, deterministik trend modeli kullanılabilir.
\\end{itemize}

Durağanlık analizi, zaman serisi modellemesinde kritik bir adımdır. Durağan olmayan serilerin kullanımı, sahte regresyon problemine yol açabilir ve güvenilir olmayan tahminler üretebilir. Bu nedenle, zaman serisi analizine başlamadan önce serilerin durağanlık özelliklerinin incelenmesi ve gerekirse uygun dönüşümlerin yapılması önemlidir.
"""
    return info_text

def main():
    try:
        print("Veri dosyası okunuyor...")
        # Veri okuma
        excel_file = 'data/emission_dataset_revised.xlsx'
        xl = pd.ExcelFile(excel_file)
        
        all_latex_tables = ""
        
        for sheet_name in xl.sheet_names:
            print(f"Çalışma sayfası işleniyor: {sheet_name}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            print(f"Veri başarıyla okundu. Sütunlar: {df.columns.tolist()}")
            
            # Test sonuçlarını saklamak için liste
            test_results = []
            
            # Her bir sayısal sütun için Fuller testi uygula
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            print(f"Sayısal sütunlar: {numeric_columns.tolist()}")
            
            for column in numeric_columns:
                result = perform_fuller_test(df[column], column)
                test_results.append(result)
            
            print(f"{sheet_name} için LaTeX tablosu oluşturuluyor...")
            # LaTeX tablosu oluştur
            latex_table = create_latex_table(test_results, sheet_name)
            all_latex_tables += latex_table + "\n"
        
        # Tüm tabloları içeren LaTeX dosyasını oluştur
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        latex_document = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{booktabs}}
\\usepackage{{float}}
\\usepackage{{siunitx}}
\\usepackage{{threeparttable}}
\\usepackage{{caption}}

\\title{{Emisyon Verilerinin Durağanlık Analizi}}
\\author{{İstatistik Analiz Grubu}}
\\date{{Rapor Tarihi: {timestamp}}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
Bu rapor, emisyon veri setinin durağanlık özelliklerini Fuller (Dickey-Fuller) testi kullanarak incelemektedir. Test sonuçları, veri setinin durağanlık özelliklerini belirlemek için kullanılmış ve sonuçlar detaylı bir şekilde raporlanmıştır.
\\end{{abstract}}

\\newpage

{create_info_text()}

\\newpage

"""
        latex_document += all_latex_tables
        latex_document += "\\end{document}"
        
        # Sonuçları kaydet
        results_dir = '../6811fd596a78452ac1f2ded6/results'
        os.makedirs(results_dir, exist_ok=True)
        
        output_file = f'{results_dir}/fuller_test_results_all_{datetime.now().strftime("%Y%m%d_%H%M%S")}.tex'
        print(f"Sonuçlar kaydediliyor: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_document)
        
        print("Git işlemleri başlatılıyor...")
        # Git komutlarını çalıştır
        os.chdir('../6811fd596a78452ac1f2ded6')
        
        # Git durumunu kontrol et
        if os.system('git status') != 0:
            print("Git deposu başlatılıyor...")
            os.system('git init')
            os.system('git remote add origin https://git.overleaf.com/6811fd596a78452ac1f2ded6')
        
        # Değişiklikleri ekle ve commit et
        os.system('git add results/fuller_test_results_*.tex')
        os.system('git commit -m "Fuller durağanlık testi sonuçları güncellendi"')
        
        # Uzak depodaki değişiklikleri çek
        os.system('git pull origin master')
        
        # Değişiklikleri gönder
        os.system('git push origin master')
        
        print("İşlem tamamlandı!")
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        raise

if __name__ == "__main__":
    main() 