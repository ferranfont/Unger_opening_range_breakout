# Sistema que lee y formatea data de Ninjatrader

from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
#import chart
#import plotly_chart as chart
#import plotly_chart_volume as chart
import plotly_chart as chart
import config
import os
now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
load_dotenv()

# Parámetros del Sistema
fecha = "2025-04-24"  # Fecha de inicio para el cuadradito
hora = "15:30:00"     # Hora de inicio para el cuadradito
lookback_min = 120    # Ventana de tiempo en minutos para el cuadradito

START_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
END_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
END_TIME = pd.Timestamp(f'{fecha} {hora}', tz='Europe/Madrid')
START_TIME = END_TIME - pd.Timedelta(minutes=lookback_min)

print("\nRangos:")
print(f"Start date: {START_DATE}, \nEnd date: {END_DATE}, \nStart time: {START_TIME}, \nEnd time: {END_TIME}")

# Dataset con toda la data desde el 2015 hasta el 2025  
directorio = '../DATA'
nombre_fichero = 'export_es_2015_formatted.csv'
ruta_completa = os.path.join(directorio, nombre_fichero)
print('\nFichero:', ruta_completa, 'importado')
df = pd.read_csv(ruta_completa)

print("\nFull Dataset:")
print(df)

# CREACIÓN DE UN SUBDATASET CON UN RANGO 
#   Convertir los límites de fecha
# Asegurarte de que 'Date' está presente
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], utc=True)  # Asegura que tiene zona horaria UTC
    df.set_index('Date', inplace=True)
df.index = df.index.tz_convert('Europe/Madrid')

# Filtrar el rango de fechas
df_subset = df[(df.index.date >= START_DATE.date()) & (df.index.date <= END_DATE.date())]

print(f"✅ Subdataset creado con {len(df_subset)} registros entre {START_DATE} y {END_DATE}")
print(df_subset)

# Graficación del dataset
formated_titulo = START_DATE.strftime('%Y-%m-%d')
titulo = f"SP500 en fecha {formated_titulo}_plotted on_{now_str}"
y0_value, y1_value = chart.graficar_precio(df_subset, titulo, START_DATE, END_DATE, START_TIME, END_TIME)
opening_range = y1_value - y0_value

print(f"\nMínimo del Rango: {y0_value}")
print(f"Màximo del Rango: {y1_value}")
print(f"Rango Apertura: {opening_range}")

