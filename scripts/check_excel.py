import pandas as pd

# Excel dosyasını oku
df = pd.read_excel('../data/emission_dataset.xlsx', sheet_name='ek1')

# Veri seti hakkında bilgi
print("Veri Seti Boyutu:", df.shape)
print("\nSütunlar:", df.columns.tolist())
print("\nVeri Tipleri:\n", df.dtypes)
print("\nİlk 5 Satır:\n", df.head())
print("\nEksik Değerler:\n", df.isnull().sum()) 