# ANDREA UNGER TRADING SYSTEM BREAK OUT OPENING RANGE
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
#import chart
#import plotly_chart as chart
#import plotly_chart_volume as chart
import plotly_chart as chart
import tops_and_bottoms_fractals as tops
#import order_managment as om
import order_entry_managment as oem
import config
import os
now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
load_dotenv()

# Parámetros del Sistema
fecha = "2025-04-17"  # Fecha de inicio para el cuadradito
hora = "15:30:00"     # Hora de inicio para el cuadradito
lookback_min = 60    # Ventana de tiempo en minutos para el cuadradito
entry_shift = 1      # Desplazamiento para la entrada (1 punto por encima del fractal)

START_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
END_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
END_TIME = pd.Timestamp(f'{fecha} {hora}', tz='Europe/Madrid')
START_TIME = END_TIME - pd.Timedelta(minutes=lookback_min)

print("\nRangos:")
print(f"Start date: {START_DATE}, \nEnd date: {END_DATE}, \nStart time: {START_TIME}, \nEnd time: {END_TIME}")

# Initialize all variables to None to avoid NameError
first_breakout_pauta_plana_price = None
first_breakout_pauta_plana_time = None
first_breakout_bool = False
first_breakdown_bool = False
patito_negro_bool = False
first_breakout_time = None
first_breakout_price = None
first_breakdown_time = None
first_breakdown_price = None
target_filled_time = None
target_profit = None
stop_lost_time = None
stop_lost = None
patito_negro_time = None

# ====================================================
# 📥 DESCARGA DE DATOS 
# ====================================================
directorio = '../DATA'
nombre_fichero = 'export_es_2015_formatted.csv'
ruta_completa = os.path.join(directorio, nombre_fichero)
print('\nFichero:', ruta_completa, 'importado')
df = pd.read_csv(ruta_completa)

print("\n=============== 🔍 df  ===============")
print(df)
print(f"Segment Shape: {df.shape}")
# CREACIÓN DE UN SUBDATASET CON UN RANGO 
# Convertir los límites de fecha
# Asegurarte de que 'Date' está presente
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], utc=True)  # Asegura que tiene zona horaria UTC
    df.set_index('Date', inplace=True)
df.index = df.index.tz_convert('Europe/Madrid')

# Filtrar el rango de fechas
df_subset = df[(df.index.date >= START_DATE.date()) & (df.index.date <= END_DATE.date())]

print("\n=============== 🔍 df_subset  ==============")
print(f"✅ Subdataset: Creado con {len(df_subset)} registros entre {START_DATE} y {END_DATE}")
print(df_subset)
print(f"Segment Shape: {df_subset.shape}")


# ====================================================
# 📉 BUSQUEDA DEL MÁXIMO Y MÍNIMO DEL CUADRADITO 
# ====================================================
window_df = df[(df.index >= START_TIME) & (df.index <= END_TIME)]

if not window_df.empty:
    y0_value = window_df['Low'].min()
    y1_value = window_df['High'].max()

opening_range = y1_value - y0_value

print(f"\nMínimo del Rango del Cuadradito: {y0_value}")
print(f"Màximo del Rango del Cuadradito: {y1_value}")
print(f"Rango Apertura del Cuadradito: {opening_range}")

# Filter only data after END_TIME (15:30)- BUSCAMOS ENTRAR TAN SÓLO DESPUÉS DE LAS 15:30
after_open_df = df_subset[df_subset.index >= END_TIME]

# ====================================================
# 💣 ROTURA DEL CUADRADITO
# ====================================================
breakout_rows = after_open_df[after_open_df['High'] > y1_value]
if not breakout_rows.empty:
    first_breakout_time = breakout_rows.index[0]
    first_breakout_price = breakout_rows.iloc[0]['High']
    first_breakout_bool = True
    print(f"⚡ High_Breakout_Range at {first_breakout_time} with price {first_breakout_price}")

# Check for low breakdown
breakdown_rows = after_open_df[after_open_df['Low'] < y0_value]
if not breakdown_rows.empty:
    first_breakdown_time = breakdown_rows.index[0]
    first_breakdown_price = breakdown_rows.iloc[0]['Low']
    print(f"⚡ Low_Breakdown at Range {first_breakdown_time} with price {first_breakdown_price}")

# ====================================================
#  🦢 BUSQUEDA DE PAUTA PLANA DESPUÉS DE LA ROTURA 
# ====================================================
tops_df = tops.find_first_strong_top(after_open_df, shifts=[1, 2], min_diff=0, y0_value=y0_value, y1_value=y1_value)
print("\nPauta Plana_Tops encontrados:")
print(tops_df)
patito_negro = tops_df.iloc[0]['High']
patito_negro_time = tops_df.index[0]
patito_negro_bool = True

print(f"✅ Entraremos en la primera rotura del nivel: {patito_negro} a las {patito_negro_time}")

# Detect first breakout over Patito Negro, ENTRADA AL MERCADO
if first_breakout_bool and patito_negro_bool:
    breakout_pauta_plana = after_open_df[
        (after_open_df.index >= patito_negro_time) &
        (after_open_df['Close'] > patito_negro)
    ]
    if not breakout_pauta_plana.empty:
        first_breakout_pauta_plana_time = breakout_pauta_plana.index[0]
        first_breakout_pauta_plana_price = breakout_pauta_plana.iloc[0]['Close']

# ====================================================
#  🖨️ PRINTS
# ====================================================
print("\n=================📊 MARKET PARAMETERS =================")
print(f"🔹 Y1 Value: {y1_value}")
print(f"🔹 Y0 Value: {y0_value}")
print(f"📏 Opening Range: {opening_range}")

print(f"⚡ First Breakout Bool: {first_breakout_bool}")
print(f"🕒 First Breakout Time: {first_breakout_time}")
print(f"💲 First Breakout Price: {first_breakout_price}")

print(f"⚡ First Breakdown Bool: {first_breakdown_bool}")
print(f"🕒 First Breakdown Time: {first_breakdown_time}")
print(f"💲 First Breakdown Price: {first_breakdown_price}")

print(f"⚡ Fractal Patito Negro Bool(Pauta Plana): {patito_negro_bool}")
print(f"🕒 Fractal Patito Negro Time(Pauta Plana): {patito_negro_time}")
print(f"💲 Fractal Patito Negro Price(Pauta Plana): {patito_negro}")

print(f"💡 Buy Entry Time : {first_breakout_pauta_plana_time}")
print(f"💡 Buy Entry Price: {first_breakout_pauta_plana_price}")

print("===================================================\n")

# ===============================
# 📞 CALL ORDER MANAGEMENT FUNCTION + ENTRADA AL MERCADO
# ===============================
trade_result = oem.order_management_with_iterrows(
    after_open_df=after_open_df,
    y0_value=y0_value,
    y1_value=y1_value,
    opening_range=opening_range,
    END_TIME=END_TIME,
    patito_negro=patito_negro,
    first_breakout_bool=first_breakout_bool,
    first_breakout_time=first_breakout_time,
    first_breakout_price=first_breakout_price,
    first_breakdown_bool=first_breakdown_bool,
    first_breakdown_time=first_breakdown_time,
    first_breakdown_price=first_breakdown_price,
    patito_negro_bool=patito_negro_bool,
    patito_negro_time=patito_negro_time,
    first_breakout_pauta_plana_price=first_breakout_pauta_plana_price,
    first_breakout_pauta_plana_time=first_breakout_pauta_plana_time
)


# GRAFICACIÓN DE DATOS 
# ====================================================
formated_titulo = START_DATE.strftime('%Y-%m-%d')
titulo = f"SP500 en fecha {formated_titulo}_plotted on_{now_str}"
exit_time = trade_result['exit_trade_time']
exit_price = trade_result['exit_trade_price']

formated_titulo = START_DATE.strftime('%Y-%m-%d')
titulo = f"SP500 en fecha {formated_titulo}_plotted on_{now_str}"

exit_time = trade_result['exit_trade_time']
exit_price = trade_result['exit_trade_price']

chart.graficar_precio(
    df_subset,
    titulo,
    START_TIME,
    END_TIME,
    y0_value,
    y1_value,
    patito_negro_time,
    patito_negro,
    first_breakout_pauta_plana_time,
    first_breakout_pauta_plana_price,
    exit_time,
    exit_price
)

print("\n=============== 📈 SUMMARY TRADE RESULT ================")
summary_output_df = pd.DataFrame([trade_result])
print(summary_output_df.T)
print("===========================================================\n")

# Save into a CSV and ceate the output DataFrame to be stored
output_df = pd.DataFrame([trade_result])

# Make sure outputs directory exists
os.makedirs('outputs', exist_ok=True)

# Define the CSV file path
summary_file_path = os.path.join('outputs', 'summary_output_df.csv')

# Check if the file exists
if os.path.exists(summary_file_path):
    # If it exists, read the existing CSV
    existing_df = pd.read_csv(summary_file_path)
    
    # Append the new row (aligning columns)
    updated_df = pd.concat([existing_df, output_df], ignore_index=True)
    
    # Write the updated DataFrame back to CSV
    updated_df.to_csv(summary_file_path, index=False)
    print(f"✅ Summary updated and saved to {summary_file_path}")
else:
    # If it doesn't exist, create it with the new data
    output_df.to_csv(summary_file_path, index=False)
    print(f"✅ Summary created and saved to {summary_file_path}")
