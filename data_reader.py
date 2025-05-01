import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import pytz
os.makedirs('charts', exist_ok=True)


# Ruta al archivo y DATA RAW DE NINJATRADER
directorio = '../DATA'
#nombre_fichero = 'export_es_2015.csv'
#nombre_fichero = 'export_NQ_2015.csv'
#nombre_fichero = 'export_6E_2015.csv'
#nombre_fichero = 'export_YM_2015.csv'
nombre_fichero = 'export_GC_2015.csv'



ruta_completa = os.path.join(directorio, nombre_fichero)

# Definir los nombres manualmente si saltas la cabecera
columnas = ['Date', 'Open', 'High', 'Low', 'Close', 'Volumen']

# Leer el archivo saltando la primera fila
df = pd.read_csv(
    ruta_completa,
    sep=';',
    decimal=',',
    encoding='utf-8',
    skiprows=1,
    names=columnas
)

# Convert to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Localize as Europe/Madrid (Barcelona time)
df['Date'] = df['Date'].dt.tz_localize('Europe/Madrid', ambiguous='NaT')
df.reset_index(drop=True, inplace=True)

print(df.head())
print(df.tail())
# Mostrar tipos de datos de cada columna
print("\nTipos de datos:")
print(df.dtypes)

# Crear nombre de salida con "_formatted" antes de la extensión
nombre_salida = nombre_fichero.replace('.csv', '_formatted.csv')
ruta_salida = os.path.join(directorio, nombre_salida)

# Guardar DataFrame como CSV
df.to_csv(ruta_salida, index=False)
print(f'✅ Archivo guardado en: {ruta_salida}')

