import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import glob
import statsmodels.api as sm
import tqdm

def fourier_terms(t, k):
    """
    Fourier terimlerini hesaplar
    
    Parameters:
    -----------
    t : array
        Zaman dizisi (1'den n'e kadar)
    k : int
        Fourier frekans sayısı
    
    Returns:
    --------
    array
        Fourier terimleri matrisi
    """
    n = len(t)
    fourier_matrix = np.zeros((n, 2*k))
    for i in range(k):
        fourier_matrix[:, 2*i] = np.sin(2 * np.pi * (i+1) * t / n)
        fourier_matrix[:, 2*i+1] = np.cos(2 * np.pi * (i+1) * t / n)
    return fourier_matrix

def block_bootstrap(data, block_size, n_samples):
    """
    Zaman serisi için block bootstrap örneklemesi yapar
    
    Parameters:
    -----------
    data : array
        Orijinal zaman serisi
    block_size : int
        Blok uzunluğu
    n_samples : int
        Bootstrap örnek uzunluğu (genellikle orijinal seri uzunluğu)
    
    Returns:
    --------
    array
        Block bootstrap ile üretilmiş yeni seri
    """
    n = len(data)
    n_blocks = int(np.ceil(n_samples / block_size))
    blocks = []
    for _ in range(n_blocks):
        start = np.random.randint(0, n - block_size + 1)
        block = data[start:start+block_size]
        blocks.append(block)
    bootstrapped = np.concatenate(blocks)[:n_samples]
    return bootstrapped

def bootstrap_critical_values(data, column_name, n_bootstrap=1000, max_k=3, block_size=5, random_state=42):
    """
    Block bootstrap ile Fourier ADF test istatistiği için kritik değerleri belirler
    """
    np.random.seed(random_state)
    n = len(data)
    boot_stats = []
    for _ in range(n_bootstrap):
        resampled = block_bootstrap(data, block_size=block_size, n_samples=n)
        try:
            stat = perform_fourier_adf_test(resampled, column_name, max_k=max_k, use_bootstrap=False)['test_statistic']
            if stat is not None:
                boot_stats.append(stat)
        except:
            continue
    boot_stats = np.sort(boot_stats)
    crit_1 = np.percentile(boot_stats, 1)
    crit_5 = np.percentile(boot_stats, 5)
    crit_10 = np.percentile(boot_stats, 10)
    return {'1%': crit_1, '5%': crit_5, '10%': crit_10}

def perform_fourier_adf_test(data, column_name, max_k=3, use_bootstrap=False, n_bootstrap=1000, block_size=5):
    """
    Fourier ADF durağanlık testi uygular (isteğe bağlı bootstrap kritik değer)
    """
    try:
        y = np.array(data)
        n = len(y)
        if n < 10:
            return {
                'variable': column_name,
                'test_statistic': None,
                'p_value': None,
                'critical_values': None,
                'optimal_k': None,
                'n_obs': n,
                'result': 'Yetersiz gözlem sayısı'
            }
        if len(np.unique(y)) < 2:
            return {
                'variable': column_name,
                'test_statistic': None,
                'p_value': None,
                'critical_values': None,
                'optimal_k': None,
                'n_obs': n,
                'result': 'Sabit değer'
            }
        y = y[~np.isnan(y)]
        if len(y) < 10:
            return {
                'variable': column_name,
                'test_statistic': None,
                'p_value': None,
                'critical_values': None,
                'optimal_k': None,
                'n_obs': len(y),
                'result': 'NaN değerler temizlendikten sonra yetersiz gözlem'
            }
        try:
            adf_result = adfuller(y)
            adf_stat = adf_result[0]
            adf_pval = adf_result[1]
            adf_crit = adf_result[4]
        except:
            return {
                'variable': column_name,
                'test_statistic': None,
                'p_value': None,
                'critical_values': None,
                'optimal_k': None,
                'n_obs': len(y),
                'result': 'ADF testi hatası'
            }
        best_k = 0
        best_aic = float('inf')
        for k in range(1, max_k + 1):
            try:
                t = np.arange(1, n + 1)
                fourier = fourier_terms(t, k)
                X = np.column_stack([np.ones(n), t, fourier])
                model = sm.OLS(y, X).fit()
                aic = model.aic
                if aic < best_aic:
                    best_aic = aic
                    best_k = k
            except:
                continue
        if best_k == 0:
            return {
                'variable': column_name,
                'test_statistic': adf_stat,
                'p_value': adf_pval,
                'critical_values': adf_crit,
                'optimal_k': 0,
                'n_obs': len(y),
                'result': 'Fourier terimleri eklenemedi'
            }
        try:
            t = np.arange(1, n + 1)
            fourier = fourier_terms(t, best_k)
            X = np.column_stack([np.ones(n), t, fourier])
            model = sm.OLS(y, X).fit()
            test_stat = model.tvalues[1]
            p_value = model.pvalues[1]
            # --- Bootstrap kritik değerler ---
            if use_bootstrap:
                crit_values = bootstrap_critical_values(y, column_name, n_bootstrap=n_bootstrap, max_k=max_k, block_size=block_size)
            else:
                crit_values = {'1%': -3.43, '5%': -2.86, '10%': -2.57}
            if test_stat < crit_values['1%']:
                result = 'Durağan (1%)'
            elif test_stat < crit_values['5%']:
                result = 'Durağan (5%)'
            elif test_stat < crit_values['10%']:
                result = 'Durağan (10%)'
            else:
                result = 'Durağan Değil'
            return {
                'variable': column_name,
                'test_statistic': test_stat,
                'p_value': p_value,
                'critical_values': crit_values,
                'optimal_k': best_k,
                'n_obs': len(y),
                'result': result
            }
        except:
            return {
                'variable': column_name,
                'test_statistic': adf_stat,
                'p_value': adf_pval,
                'critical_values': adf_crit,
                'optimal_k': best_k,
                'n_obs': len(y),
                'result': 'Fourier ADF testi hatası'
            }
    except Exception as e:
        return {
            'variable': column_name,
            'test_statistic': None,
            'p_value': None,
            'critical_values': None,
            'optimal_k': None,
            'n_obs': None,
            'result': f'Test hatası: {str(e)}'
        }

def perform_fourier_adf_test_with_differences(data, column_name, max_k=3, max_diff=2, use_bootstrap=True, n_bootstrap=1000, block_size=5):
    results = []
    current_data = np.array(data)
    result = perform_fourier_adf_test(current_data, f"{column_name} (Orijinal)", max_k=max_k, use_bootstrap=use_bootstrap, n_bootstrap=n_bootstrap, block_size=block_size)
    result['fark_seviyesi'] = 0
    results.append(result)
    for diff_level in range(1, max_diff + 1):
        current_data = np.diff(current_data)
        current_data = current_data[~np.isnan(current_data)]
        if len(current_data) < 10:
            results.append({
                'variable': f"{column_name} (Fark {diff_level})",
                'test_statistic': None,
                'p_value': None,
                'critical_values': None,
                'optimal_k': None,
                'n_obs': len(current_data),
                'result': 'Yetersiz gözlem sayısı',
                'fark_seviyesi': diff_level
            })
            continue
        result = perform_fourier_adf_test(current_data, f"{column_name} (Fark {diff_level})", max_k=max_k, use_bootstrap=use_bootstrap, n_bootstrap=n_bootstrap, block_size=block_size)
        result['fark_seviyesi'] = diff_level
        results.append(result)
        if result['result'].startswith('Durağan'):
            break
    return results

def create_latex_table_with_differences(results, sheet_name):
    """
    Fark seviyelerini içeren LaTeX tablosu oluşturur
    
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
    if sheet_name == 'perakende':
        rows_per_page = 40
        total_pages = (len(results) + rows_per_page - 1) // rows_per_page
        all_tables = ""
        
        for page in range(total_pages):
            start_idx = page * rows_per_page
            end_idx = min((page + 1) * rows_per_page, len(results))
            current_results = results[start_idx:end_idx]
            
            table = f"""\\begin{{table}}[H]
\\centering
\\resizebox{{\\textwidth}}{{!}}{{% 
\\begin{{threeparttable}}
\\caption{{Fourier ADF Durağanlık Testi Sonuçları (Fark Analizi) - {sheet_name} ({page + 1}/{total_pages})}}
\\label{{tab:fourier_adf_test_diff_{sheet_name}_{page + 1}}}
\\begin{{tabular}}{{lS[table-format=-2.4]S[table-format=1.4]S[table-format=-2.4]S[table-format=-2.4]cl}}
\\toprule
Değişken & {{FADF İst.}} & {{p-değeri}} & {{1\\%}} & {{5\\%}} & {{k}} & {{Sonuç}} \\\\
\\midrule
"""
            
            for result in current_results:
                sanitized_variable = sanitize_latex_variable(result['variable'])
                if result['test_statistic'] is None:
                    table += f"{sanitized_variable} & {{--}} & {{--}} & {{--}} & {{--}} & {{--}} & {result['result']} \\\\\n"
                else:
                    table += f"{sanitized_variable} & {result['test_statistic']:.4f} & {result['p_value']:.4f} & "
                    table += f"{result['critical_values']['1%']:.4f} & {result['critical_values']['5%']:.4f} & "
                    table += f"{result['optimal_k']} & {result['result']} \\\\\n"
            
            table += """\\bottomrule
\\end{tabular}
\\begin{tablenotes}
\\small
\\item[1] H0: Seri durağan değil (birim kök var)
\\item[2] H1: Seri durağan (birim kök yok)
\\item[3] Kritik değerler: MacKinnon (1996)
\\item[4] k: Optimal Fourier frekans sayısı
\\end{tablenotes}
\\end{threeparttable}
}}
\\end{table}
\\newpage
"""
            all_tables += table
        
        return all_tables
    
    else:
        latex_table = f"""\\begin{{table}}[H]
\\centering
\\resizebox{{\\textwidth}}{{!}}{{% 
\\begin{{threeparttable}}
\\caption{{Fourier ADF Durağanlık Testi Sonuçları (Fark Analizi) - {sheet_name}}}
\\label{{tab:fourier_adf_test_diff_{sheet_name}}}
\\begin{{tabular}}{{lS[table-format=-2.4]S[table-format=1.4]S[table-format=-2.4]S[table-format=-2.4]cl}}
\\toprule
Değişken & {{FADF İst.}} & {{p-değeri}} & {{1\\%}} & {{5\\%}} & {{k}} & {{Sonuç}} \\\\
\\midrule
"""
        
        for result in results:
            sanitized_variable = sanitize_latex_variable(result['variable'])
            if result['test_statistic'] is None:
                latex_table += f"{sanitized_variable} & {{--}} & {{--}} & {{--}} & {{--}} & {{--}} & {result['result']} \\\\\n"
            else:
                latex_table += f"{sanitized_variable} & {result['test_statistic']:.4f} & {result['p_value']:.4f} & "
                latex_table += f"{result['critical_values']['1%']:.4f} & {result['critical_values']['5%']:.4f} & "
                latex_table += f"{result['optimal_k']} & {result['result']} \\\\\n"
        
        latex_table += """\\bottomrule
\\end{tabular}
\\begin{tablenotes}
\\small
\\item[1] H0: Seri durağan değil (birim kök var)
\\item[2] H1: Seri durağan (birim kök yok)
\\item[3] Kritik değerler: MacKinnon (1996)
\\item[4] k: Optimal Fourier frekans sayısı
\\end{tablenotes}
\\end{threeparttable}
}}
\\end{table}
\\newpage
"""
        
        return latex_table

def sanitize_latex_variable(variable_name):
    """
    Değişken adını LaTeX uyumlu hale getirir
    
    Parameters:
    -----------
    variable_name : str
        Orijinal değişken adı
    
    Returns:
    --------
    str
        LaTeX uyumlu değişken adı
    """
    # Özel karakterleri escape et
    replacements = {
        '_': ' ',  # alt çizgiyi boşluğa çevir
        '%': '\\%',  # yüzde işaretini escape et
        '#': '\\#',  # diyez işaretini escape et
        '$': '\\$',  # dolar işaretini escape et
        '&': '\\&',  # ve işaretini escape et
        '{': '\\{',  # süslü parantezleri escape et
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
        '\\': '\\textbackslash{}',
        '<': '\\textless{}',
        '>': '\\textgreater{}',
        '≤': '$\\leq$',
        '≥': '$\\geq$',
        '/': '/',
        '–': '--'
    }
    
    result = variable_name
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    
    return result

def create_info_text():
    """
    Fourier ADF testi hakkında detaylı bilgi metni oluşturur
    
    Returns:
    --------
    str
        Bilgi metni
    """
    info_text = """\\section{Fourier ADF Durağanlık Testi Hakkında}

Fourier ADF (FADF) durağanlık testi, geleneksel ADF testinin Fourier fonksiyonları ile genişletilmiş bir versiyonudur. Bu test, zaman serilerindeki yapısal kırılmaları ve doğrusal olmayan trendi daha iyi yakalayabilmektedir.

\\subsection{Test Formülü}

FADF testi için kullanılan model:

\\[
\\Delta y_t = \\alpha + \\beta t + \\gamma y_{t-1} + \\sum_{k=1}^K [\\delta_{k,1} \\sin(\\frac{2\\pi kt}{T}) + \\delta_{k,2} \\cos(\\frac{2\\pi kt}{T})] + \\sum_{j=1}^p \\phi_j \\Delta y_{t-j} + \\varepsilon_t
\\]

Burada:
\\begin{itemize}
    \\item $\\Delta y_t$: Serinin birinci farkı
    \\item $\\alpha$: Sabit terim
    \\item $\\beta t$: Trend terimi
    \\item $\\gamma$: Test edilecek parametre
    \\item $k$: Fourier frekans sayısı
    \\item $T$: Örneklem büyüklüğü
    \\item $\\varepsilon_t$: Hata terimi
    \\item $\\sin(\\frac{2\\pi kt}{T})$ ve $\\cos(\\frac{2\\pi kt}{T})$: Fourier terimleri
\\end{itemize}

\\subsection{Hipotezler}

\\begin{itemize}
    \\item $H_0: \\gamma = 0$ (Seri durağan değil, birim kök içerir)
    \\item $H_1: \\gamma < 0$ (Seri durağandır)
\\end{itemize}

\\subsection{Test Sonuçlarının Detaylı Yorumlanması}

\\begin{itemize}
    \\item \\textbf{FADF İstatistiği:} Test istatistiği. Bu değer, kritik değerlerle karşılaştırılır. Eğer FADF istatistiği kritik değerlerden daha küçükse (daha negatifse), null hipotezi reddedilir ve seri durağan kabul edilir.
    
    \\item \\textbf{p-değeri:} Bu değer, null hipotezinin reddedilme olasılığını gösterir. Genellikle 0.05 eşik değeri kullanılır:
    \\begin{itemize}
        \\item p-değeri < 0.05 ise, null hipotezi reddedilir ve seri durağan kabul edilir.
        \\item p-değeri > 0.05 ise, null hipotezi reddedilemez ve seri durağan değil kabul edilir.
    \\end{itemize}
    
    \\item \\textbf{Kritik Değerler:} Farklı anlamlılık düzeyleri (genellikle \\%1, \\%5 ve \\%10) için eşik değerlerdir. FADF istatistiği bu değerlerden küçükse, ilgili anlamlılık düzeyinde seri durağan kabul edilir.
    
    \\item \\textbf{Optimal k:} En uygun Fourier frekans sayısı. Bu değer, AIC kriterine göre seçilir ve modelin yapısal kırılmaları ne kadar iyi yakaladığını gösterir.
    
    \\item \\textbf{Gözlem Sayısı:} Analizde kullanılan veri noktalarının sayısı. Daha fazla gözlem, genellikle daha güvenilir sonuçlar verir.
    
    \\item \\textbf{Sonuç:} "Durağan" veya "Durağan Değil" şeklinde özetlenir. Bu sonuç, p-değerine dayanarak belirlenir.
\\end{itemize}

\\subsection{Fourier ADF Testinin Avantajları}

\\begin{itemize}
    \\item \\textbf{Yapısal Kırılmalar:} Fourier terimleri sayesinde, serideki yapısal kırılmaları önceden bilmeye gerek kalmadan tespit edebilir.
    
    \\item \\textbf{Doğrusal Olmayan Trend:} Trigonometrik terimler kullanarak doğrusal olmayan trendi yakalayabilir.
    
    \\item \\textbf{Esneklik:} Farklı frekans sayıları (k) denenerek en uygun model seçilebilir.
    
    \\item \\textbf{Güç:} Geleneksel ADF testine göre daha güçlü sonuçlar verebilir, özellikle yapısal kırılmalar ve doğrusal olmayan trend varlığında.
\\end{itemize}

Fourier ADF testi, özellikle ekonomik ve finansal zaman serilerinde sıkça karşılaşılan yapısal kırılmaları ve doğrusal olmayan trendi dikkate alarak daha güvenilir durağanlık analizi yapılmasını sağlar. Bu özelliği ile geleneksel ADF testine göre daha kapsamlı bir analiz sunar.
"""
    return info_text

def main():
    try:
        print("Veri dosyası okunuyor...")
        excel_file = 'data/emission_dataset_revised.xlsx'
        xl = pd.ExcelFile(excel_file)
        
        # LaTeX başlangıç
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        latex_document = f"""\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{booktabs}}
\\usepackage{{float}}
\\usepackage{{siunitx}}
\\usepackage{{threeparttable}}
\\usepackage{{caption}}
\\usepackage{{graphicx}}
\\usepackage[a4paper,margin=2.5cm]{{geometry}}
\\usepackage{{amsmath}}

\\title{{Emisyon Verilerinin Fourier ADF Durağanlık Analizi (Fark Analizi)}}
\\author{{İstatistik Analiz Grubu}}
\\date{{Rapor Tarihi: {timestamp}}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
Bu rapor, emisyon veri setinin durağanlık özelliklerini Fourier ADF (FADF) testi kullanarak incelemektedir. 
FADF testi, geleneksel ADF testinin Fourier fonksiyonları ile genişletilmiş bir versiyonudur ve yapısal 
kırılmaları daha iyi yakalayabilmektedir. Test sonuçları, veri setinin durağanlık özelliklerini belirlemek 
için kullanılmış ve sonuçlar detaylı bir şekilde raporlanmıştır. Ayrıca, durağan olmayan seriler için fark 
analizi yapılmış ve serilerin entegrasyon dereceleri belirlenmiştir.
\\end{{abstract}}

\\newpage

{create_info_text()}

\\newpage

"""
        
        all_latex_tables = ""
        
        for sheet_name in xl.sheet_names:
            print(f"Çalışma sayfası işleniyor: {sheet_name}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            print(f"Veri başarıyla okundu. Sütunlar: {df.columns.tolist()}")
            
            df = df.drop(columns=['Yıl'])
            print(f"Yıl sütunu başarıyla kaldırıldı. Sütunlar: {df.columns.tolist()}")
            
            all_test_results = []
            numeric_columns = list(df.select_dtypes(include=[np.number]).columns)
            print(f"Sayısal sütunlar: {numeric_columns}")
            
            for column in numeric_columns:
                results = perform_fourier_adf_test_with_differences(df[column], column)
                all_test_results.extend(results)
            
            print(f"{sheet_name} için LaTeX tablosu oluşturuluyor...")
            latex_table = create_latex_table_with_differences(all_test_results, sheet_name)
            all_latex_tables += latex_table
        
        latex_document += all_latex_tables
        latex_document += "\\end{document}"
        
        results_dir = '../6811fd596a78452ac1f2ded6/results'
        os.makedirs(results_dir, exist_ok=True)
        
        output_file = f'{results_dir}/fourier_adf_test_results_with_differences_{datetime.now().strftime("%Y%m%d_%H%M%S")}.tex'
        print(f"Sonuçlar kaydediliyor: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_document)
        
        print("Git işlemleri başlatılıyor...")
        os.chdir('../6811fd596a78452ac1f2ded6')
        
        if os.system('git status') != 0:
            print("Git deposu başlatılıyor...")
            os.system('git init')
            os.system('git remote add origin https://git.overleaf.com/6811fd596a78452ac1f2ded6')
        
        os.system('git add results/fourier_adf_test_results_with_differences_*.tex')
        os.system('git commit -m "Fourier ADF durağanlık testi sonuçları (fark analizi) eklendi"')
        os.system('git pull origin master')
        os.system('git push origin master')
        
        print("İşlem tamamlandı!")
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        raise

if __name__ == "__main__":
    main() 