# Este código extrae un vector de fechas (unique) del fichero de datos.
import pandas as pd
import os

# ====================================================
# 📥 LOAD DATA
# ====================================================
directorio = '../DATA'
nombre_fichero = 'export_es_2015_formatted.csv'
ruta_completa = os.path.join(directorio, nombre_fichero)
print('\nFichero:', ruta_completa, 'importado')
df = pd.read_csv(ruta_completa)

print("\n=============== 🔍 df  ===============")
print(df)
print(f"Segment Shape: {df.shape}")

# Ensure 'Date' column is present and properly converted
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_convert('Europe/Madrid')

# Extract just the date part (no time, no tz)
df['JustDate'] = df['Date'].dt.date

# Get unique dates as date objects
unique_dates = df['JustDate'].unique()

# Convert to sorted list of strings in YYYY-MM-DD format
date_list = sorted([d.strftime('%Y-%m-%d') for d in pd.to_datetime(unique_dates)])

last_100_dates = date_list[-100:]


#print("✅ List of unique dates:", date_list)
print("✅ Number of unique dates:", len(date_list))
print("✅ Number of unique dates:", len(last_100_dates))



# Make sure outputs directory exists
os.makedirs('outputs', exist_ok=True)

# Define the file path
output_file_path = os.path.join('outputs', 'unique_dates.txt')

# Write the dates to the file, one per line
with open(output_file_path, 'w') as f:
    for date_str in date_list:
        f.write(f"{date_str}\n")

print(f"✅ Unique dates saved to {output_file_path}")

# Define the file path for the last 100 dates
last_100_file_path = os.path.join('outputs', 'last_100_unique_dates.txt')

# Write the last 100 dates to the file, one per line
with open(last_100_file_path, 'w') as f:
    for date_str in last_100_dates:
        f.write(f"{date_str}\n")

print(f"✅ Last 100 unique dates saved to {last_100_file_path}")