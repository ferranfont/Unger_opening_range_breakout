# Sistema que lee y formatea data de Ninjatrader

from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
#import chart
import plotly_chart as chart

import config
import os
load_dotenv()

import os
import pandas as pd

# Dataset con toda la data desde el 2015 hasta el 2025  
directorio = '../DATA'
nombre_fichero = 'export_es_2015_formatted.csv'
#nombre_fichero = 'export_NQ_2015_formatted.csv'
#nombre_fichero = 'export_6E_2015_formatted.csv'
#nombre_fichero = 'export_YM_2015_formatted.csv'
#nombre_fichero = 'export_GC_2015_formatted.csv'
ruta_completa = os.path.join(directorio, nombre_fichero)
df = pd.read_csv(ruta_completa)
print(df.head())
print(df.dtypes)


# CREACIÓN DE UN SUBDATASET CON UN RANGO 
#   Convertir los límites de fecha
import pandas as pd

# Asegurarte de que 'Date' está presente
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], utc=True)  # Asegura que tiene zona horaria UTC
    df.set_index('Date', inplace=True)

# Convertir el índice a la zona horaria de Madrid
df.index = df.index.tz_convert('Europe/Madrid')

# Fechas límite
START_DATE = pd.Timestamp("2025-04-29", tz='Europe/Madrid')
END_DATE = pd.Timestamp("2025-04-29", tz='Europe/Madrid')

# Filtrar el rango de fechas
df_subset = df[(df.index >= START_DATE) & (df.index <= END_DATE)]

print(f"✅ Subdataset creado con {len(df_subset)} registros entre {START_DATE} y {END_DATE}")
print(df_subset.head())
print(df_subset.tail())



# Graficación del dataset
titulo = nombre_fichero.replace('.csv', '')
#chart.graficar_precio(df, titulo=titulo, columna='Close')
chart.graficar_precio(df_subset, titulo=titulo)


