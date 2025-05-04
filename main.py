# Sistema que lee y formatea data de Ninjatrader

from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
#import chart
#import plotly_chart as chart
#import plotly_chart_volume as chart
import plotly_chart as chart
import tops_and_bottoms_fractals as tops
import config
import os
now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
load_dotenv()

# Parámetros del Sistema
fecha = "2025-04-23"  # Fecha de inicio para el cuadradito
hora = "15:30:00"     # Hora de inicio para el cuadradito
lookback_min = 120    # Ventana de tiempo en minutos para el cuadradito

START_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
END_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
END_TIME = pd.Timestamp(f'{fecha} {hora}', tz='Europe/Madrid')
START_TIME = END_TIME - pd.Timedelta(minutes=lookback_min)

print("\nRangos:")
print(f"Start date: {START_DATE}, \nEnd date: {END_DATE}, \nStart time: {START_TIME}, \nEnd time: {END_TIME}")

# ====================================================
# DESCARGA DE DATOS 
# ====================================================

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

print(f"\n✅ Subdataset: Creado con {len(df_subset)} registros entre {START_DATE} y {END_DATE}")
print(df_subset)


# ====================================================
# BUSQUEDA DEL MÁXIMO Y MÍNIMO DEL CUADRADITO 
# ====================================================
window_df = df[(df.index >= START_TIME) & (df.index <= END_TIME)]

if not window_df.empty:
    y0_value = window_df['Low'].min()
    y1_value = window_df['High'].max()


opening_range = y1_value - y0_value

print(f"\nMínimo del Rango del Cuadradito: {y0_value}")
print(f"Màximo del Rango del Cuadradito: {y1_value}")
print(f"Rango Apertura del Cuadradito: {opening_range}")

# Filter only data after END_TIME (15:30)
after_open_df = df_subset[df_subset.index >= END_TIME]

# ====================================================
# ROTURA DEL CUADRADITO
# ====================================================

# Check for high breakout
breakout_rows = after_open_df[after_open_df['High'] > y1_value]
if not breakout_rows.empty:
    first_breakout_time = breakout_rows.index[0]
    first_breakout_price = breakout_rows.iloc[0]['High']
    print(f"\n⚡ High_Breakout_Range at {first_breakout_time} with price {first_breakout_price}")
else:
    print("\nNo High_Breakout detected after 15:30.")

# Check for low breakdown
breakdown_rows = after_open_df[after_open_df['Low'] < y0_value]
if not breakdown_rows.empty:
    first_breakdown_time = breakdown_rows.index[0]
    first_breakdown_price = breakdown_rows.iloc[0]['Low']
    print(f"⚡ Low_Breakdown at Range {first_breakdown_time} with price {first_breakdown_price}")
else:
    print("\nNo Low_Breakdown detected after 15:30.")

# ====================================================
# BUSQUEDA DE PAUTA PLANA DESPUÉS DE LA ROTURA 
# ====================================================
tops_df = tops.find_first_strong_top(after_open_df, shifts=[1, 2], min_diff=0, y0_value=y0_value, y1_value=y1_value)
print("\nPauta Plana_Tops encontrados:")
print(tops_df)
patito_negro = tops_df.iloc[0]['High']
patito_negro_time = tops_df.index[0]
print(f"✅ Entraremos en la primera rotura del nivel: {patito_negro} a las {patito_negro_time}")

# ====================================================
# ENTRADA AL MERCADO 
# ====================================================
breakout_pauta_plana = after_open_df[after_open_df['Close'] > patito_negro]
if not breakout_rows.empty:
    first_breakout_pauta_plana_time = breakout_pauta_plana.index[0]
    #first_breakout_pauta_plana_price = breakout_pauta_plana.iloc[0]['Close']  # Se entra al cierre de la Vela
    first_breakout_pauta_plana_price = patito_negro + 1  # Se entra cuando el precio cruza el nivel patito negro o máximo de la pauta plana
    print(f"\n⚡⚡⚡ Entrada -Compra- al mercado a las: {first_breakout_pauta_plana_time} en el precio {first_breakout_pauta_plana_price}")
else:
    print("\nNo High_Breakout detected after 15:30.")

# ====================================================
# GRAFICACIÓN DE DATOS 
# ====================================================
formated_titulo = START_DATE.strftime('%Y-%m-%d')
titulo = f"SP500 en fecha {formated_titulo}_plotted on_{now_str}"
chart.graficar_precio(df_subset, titulo, START_DATE, END_DATE, START_TIME, END_TIME, y0_value, y1_value, patito_negro_time, patito_negro, first_breakout_pauta_plana_time, first_breakout_pauta_plana_price)