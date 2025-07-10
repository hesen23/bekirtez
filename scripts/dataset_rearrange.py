import pandas as pd
import numpy as np
import os

def process_sheet(df, sheet_name):
    print("\nSütunlar:", df.columns.tolist())
    
    if sheet_name == 'ek4':
        # Segment ve araç tipi kombinasyonlarını pivot ile oluştur
        melted_df = pd.melt(df, id_vars=['Yıl', 'Ay', 'Segment'], 
                           value_vars=['S/D', 'H/B', 'S/W', 'MPV', 'CDV', 'Spor', 'SUV'],
                           var_name='Araç_Tipi', value_name='Adet')
        new_df = pd.pivot_table(melted_df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns=['Segment', 'Araç_Tipi'],
                              fill_value=0).reset_index()
        new_df.columns = [f"{col[0]}-{col[1]}" if isinstance(col, tuple) else col for col in new_df.columns]
    
    elif sheet_name == 'ek5':
        # Motor tiplerine göre pivot
        new_df = pd.pivot_table(df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns='Motor_Tipi',
                              fill_value=0).reset_index()
    
    elif sheet_name == 'ek6':
        # Motor cinsi ve hacmine göre pivot
        new_df = pd.pivot_table(df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns=['Motor_Cinsi', 'Motor_Hacmi'],
                              fill_value=0).reset_index()
        new_df.columns = [f"{col[0]}-{col[1]}" if isinstance(col, tuple) else col for col in new_df.columns]
    
    elif sheet_name == 'ek7':
        # Emisyon değerlerine göre pivot
        new_df = pd.pivot_table(df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns='Emisyon_Değerleri',
                              fill_value=0).reset_index()
    
    elif sheet_name == 'ek8':
        # Otomatik şanzıman tiplerine göre pivot
        new_df = pd.pivot_table(df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns='Otomatik_Sanzıman_Tipi',
                              fill_value=0).reset_index()
    
    elif sheet_name == 'ek9':
        # Hafif ticari gövde tiplerine göre pivot
        new_df = pd.pivot_table(df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns='Hafif_Ticari_Gövde_Tipi',
                              fill_value=0).reset_index()
    
    elif sheet_name == 'perakende':
        # Markalara göre pivot
        value_vars = ['Yerli_Otomobil', 'İthal_Otomobil', 'Toplam_Otomobil',
                     'Yerli_Hafif_Ticari', 'İthal_Hafif_Ticari', 'Toplam_Hafif_Ticari']
        melted_df = pd.melt(df, id_vars=['Yıl', 'Ay', 'Marka'], 
                           value_vars=value_vars,
                           var_name='Tip', value_name='Adet')
        new_df = pd.pivot_table(melted_df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns=['Marka', 'Tip'],
                              fill_value=0).reset_index()
        new_df.columns = [f"{col[0]}-{col[1]}" if isinstance(col, tuple) else col for col in new_df.columns]
    
    else:
        # Diğer sayfalar için (ek1, ek2, ek3) tek kategori sütunu
        category_col = [col for col in df.columns if col not in ['Yıl', 'Ay', 'Adet']][0]
        new_df = pd.pivot_table(df, values='Adet', 
                              index=['Yıl', 'Ay'],
                              columns=category_col,
                              fill_value=0).reset_index()
    
    print(f"İşlenen veri şekli: {new_df.shape}")
    return new_df

def main():
    print("Veri dosyası okunuyor...")
    input_file = 'data/emission_dataset.xlsx'
    
    if not os.path.exists(input_file):
        print(f"Hata: {input_file} dosyası bulunamadı!")
        return
        
    try:
        print(f"Excel dosyası açılıyor: {input_file}")
        excel_file = pd.ExcelFile(input_file)
        print(f"Bulunan sayfalar: {excel_file.sheet_names}")
        
        if len(excel_file.sheet_names) == 0:
            print("Hata: Excel dosyasında görünür çalışma sayfası bulunamadı!")
            return
            
        output_file = 'data/emission_dataset_revised.xlsx'
        print(f"İşlenmiş veriler {output_file} dosyasına kaydedilecek...")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for sheet_name in excel_file.sheet_names:
                print(f"\n{'='*50}")
                print(f"Çalışma sayfası işleniyor: {sheet_name}")
                try:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    print(f"Veri şekli: {df.shape}")
                    
                    processed_df = process_sheet(df, sheet_name)
                    
                    if processed_df is not None:
                        processed_df.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"✓ {sheet_name} sayfası başarıyla işlendi ve kaydedildi.")
                    else:
                        print(f"! {sheet_name} sayfası işlenemedi.")
                except Exception as sheet_error:
                    print(f"! {sheet_name} sayfası işlenirken hata oluştu:")
                    print(f"Hata detayı: {str(sheet_error)}")
        
        print("\nİşlem tamamlandı!")
        print(f"Veriler '{output_file}' dosyasına kaydedildi.")
    
    except Exception as e:
        print(f"\nHata oluştu: {str(e)}")
        print("Lütfen Excel dosyasının doğru formatta olduğundan ve en az bir görünür çalışma sayfası içerdiğinden emin olun.")

if __name__ == "__main__":
    main()

