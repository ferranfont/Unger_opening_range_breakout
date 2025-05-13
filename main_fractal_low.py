# ANDREA UNGER TRADING SYSTEM BREAK OUT OPENING RANGE
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
#import chart
#import plotly_chart as chart
#import plotly_chart_volume as chart
import plotly_chart_fractal_bottom as chart
import tops_and_bottoms_fractals as tops
import find_strong_bottoms as bottoms
#import order_managment as om
import order_entry_managment_fractal_low as oem
import os
now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
load_dotenv()
last_100_dates_file = os.path.join('outputs', 'last_100_unique_dates.txt')


# Read the dates from the file into a list
dates = []
if os.path.exists(last_100_dates_file):
    with open(last_100_dates_file, 'r') as f:
        dates = [line.strip() for line in f.readlines()]
    print(f"✅ Loaded {len(dates)} dates from {last_100_dates_file}")

#dates = ["2025-04-22", "2025-04-23", "2025-04-24"]
for fecha in dates:      
    print(f"\nANALIZANDO EL DIA: {fecha}")

    # Parámetros del Sistema
    #fecha = "2025-04-17"  # Fecha de inicio para el cuadradito
    hora = "15:30:00"     # Hora de inicio para el cuadradito
    lookback_min = 60    # Ventana de tiempo en minutos para el cuadradito
    entry_shift = 1      # Desplazamiento para la entrada (1 punto por encima del fractal)
    too_late_patito_negro= "19:30:00"  # Hora límite exigida para la formación del fractal patito negro para anular la entrada
    too_late_brake_fractal_pauta_plana = "20:00:00"  # Hora límite exigida para rotura del fractal patito negro para anular la entrada


    START_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
    END_DATE = pd.Timestamp(fecha, tz='Europe/Madrid')
    END_TIME = pd.Timestamp(f'{fecha} {hora}', tz='Europe/Madrid')
    START_TIME = END_TIME - pd.Timedelta(minutes=lookback_min)
    too_late_patito_negro = pd.Timestamp(f'{fecha} {too_late_patito_negro}', tz='Europe/Madrid')
    too_late_brake_fractal_pauta_plana = pd.Timestamp(f'{fecha} {too_late_patito_negro}', tz='Europe/Madrid')

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
    fractal_bottom_bool = False

    # ====================================================
    # 📥 DESCARGA DE DATOS 
    # ====================================================
    directorio = '../DATA'
    nombre_fichero = 'export_es_2015_formatted.csv'
    ruta_completa = os.path.join(directorio, nombre_fichero)
    print("\n======================== 🔍 df  ===========================")
    df = pd.read_csv(ruta_completa)
    print('Fichero:', ruta_completa, 'importado')
    print(f"Características del Fichero Base: {df.shape}")
    # leo el vector o lista con las fechas a analizar
    # ==========================================================

    # CREACIÓN DE UN SUBDATASET CON UN RANGO 
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)  # Asegura que tiene zona horaria UTC
        df.set_index('Date', inplace=True)
    df.index = df.index.tz_convert('Europe/Madrid')
    df_subset = df[(df.index.date >= START_DATE.date()) & (df.index.date <= END_DATE.date())]

    print("\n====================== 🔍 df_subset  =======================")
    print(f"Subsegmento: Creado con {len(df_subset)} registros entre {START_DATE} y {END_DATE}")
    print(f"Característica del Subsegmento: {df_subset.shape}")


    # ====================================================
    # 💣 BUSQUEDA DEL MÁXIMO Y MÍNIMO DEL CUADRADITO 
    # ====================================================
    window_df = df[(df.index >= START_TIME) & (df.index <= END_TIME)]
    if not window_df.empty:
        y0_value = window_df['Low'].min()
        y1_value = window_df['High'].max()
    opening_range = y1_value - y0_value

    print(f"\nMínimo del Rango del Cuadradito y0_value: {y0_value}")
    print(f"Màximo del Rango del Cuadradito y1_value: {y1_value}")
    print(f"Rango Apertura del Cuadradito - opening_range: {opening_range}")

    # Filter only data after END_TIME (15:30)- BUSCAMOS ENTRAR TAN SÓLO DESPUÉS DE LAS 15:30
    after_open_df = df_subset[df_subset.index >= END_TIME] # filas después de la rotura
    breakout_rows = after_open_df[after_open_df['Close'] > y1_value] # filas por encima de la rotura y1_value
    if not breakout_rows.empty:
        first_breakout_time = breakout_rows.index[0]
        first_breakout_price = breakout_rows.iloc[0]['Close']
        first_breakout_bool = True
        print(f"⚡ High_Breakout_Range TRUE at: {first_breakout_time} with price {first_breakout_price}")

    # Check for low breakdown
    breakdown_rows = after_open_df[after_open_df['Close'] < y0_value]
    if not breakdown_rows.empty:
        first_breakdown_time = breakdown_rows.index[0]
        first_breakdown_price = breakdown_rows.iloc[0]['Close']
        first_breakdown_bool = True
        print(f"⚡ Low_Breakdown TRUE at:  {first_breakdown_time} with price {first_breakdown_price}")

    # =========================================================================================
    #  🦢 BUSQUEDA DE PAUTA PLANA DESPUÉS DE LA ROTURA +  RETROCESOS CON STRONG FRACTAL LOW
    # =========================================================================================
    tops_df = tops.find_first_strong_top(after_open_df, shifts=[1, 2], min_diff=0, y0_value=y0_value, y1_value=y1_value)
    print("\nPauta Plana_Tops encontrados:")
    print(tops_df)

    if not tops_df.empty:
        patito_negro = tops_df.iloc[0]['High']
        patito_negro_time = tops_df.index[0]
        patito_negro_bool = True
        print(f"✅ Pauta Plana (patito Negro) en el nivel: {patito_negro} generado a las {patito_negro_time}")
    else:
        patito_negro = None
        patito_negro_time = None
        patito_negro_bool = False
        print("⚠️ No se encontró un fractal fuerte (patito negro) — saltando entrada para este día.")
        continue  # skip to the next date in the loop

    # Detect first breakout over Patito Negro, ENTRADA AL MERCADO
    if first_breakout_bool and patito_negro_bool:
        breakout_pauta_plana = after_open_df[
            (after_open_df.index >= patito_negro_time) &
            (after_open_df['Close'] > patito_negro)
        ]
        if not breakout_pauta_plana.empty:
            first_breakout_pauta_plana_time = breakout_pauta_plana.index[0]
            first_breakout_pauta_plana_price = breakout_pauta_plana.iloc[0]['Close']
    
    # BÚSQUEDA DE FRACTALES (LOW) en la pauta plana

    # BÚSQUEDA DE FRACTALES (LOW) SOLO DESPUÉS DEL BREAKOUT
    if first_breakout_bool:
        df_after_breakout = after_open_df[after_open_df.index >= first_breakout_time]
        fractal_bottoms_df, fractal_bottom_bool = bottoms.find_all_strong_bottoms(df_after_breakout)
    else:
        fractal_bottoms_df = pd.DataFrame()
        fractal_bottom_bool = False

    print("\nFractales bottoms en pauta plana encontrados:")
    print(fractal_bottom_bool)
    print(fractal_bottoms_df)

    if fractal_bottom_bool and not fractal_bottoms_df.empty and 'Low' in fractal_bottoms_df.columns:
        fractal_bottom_price = fractal_bottoms_df['Low'].iloc[0]
        fractal_bottom_time = fractal_bottoms_df.index[0]
    else:
        fractal_bottom_price = None
        fractal_bottom_time = None
        fractal_bottom_bool = False
        print("⚠️ No se encontró ningún fractal bottom válido tras el breakout.")
   
    # ====================================================
    #  🖨️ PRINTS
    # ====================================================
    print("\n=================📊 MARKET PARAMETERS =================")
    print(f"🔹 Y1 Value: {y1_value}")
    print(f"🔹 Y0 Value: {y0_value}")
    print(f"📏 Opening Range: {opening_range}")
    print ("\n ")
    print(f"⚡ First Breakout Bool: {first_breakout_bool}")
    print(f"🕒 First Breakout Time: {first_breakout_time}")
    print(f"⚡ First Breakdown Bool: {first_breakdown_bool}")
    print(f"🕒 First Breakdown Time: {first_breakdown_time}")
    print ("\n ")

    print(f"⚡ Fractal High Patito Negro Bool(Pauta Plana): {patito_negro_bool}")
    print(f"🕒 Fractal High Patito Negro Time(Pauta Plana): {patito_negro_time}")
    print(f"💲 Fractal High Patito Negro Price(Pauta Plana): {patito_negro}")
    print(f"⚡ Rotura de la Pauta Plana (fractal High) : {first_breakout_pauta_plana_time}\n")

    print(f"⚡ Fractal Bottom Bool(Pauta Plana): {fractal_bottom_bool}")
    print(f"🕒 Fractal Bottom Time(Pauta Plana): {fractal_bottom_time}")
    print(f"💲 Fractal Bottom Price(Pauta Plana): {fractal_bottom_price}")
    
    print("=====================================================================================\n")

    #if first_breakdown_bool == True & 
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
        first_breakout_pauta_plana_time=first_breakout_pauta_plana_time,
        fractal_bottom_bool=fractal_bottom_bool,
        fractal_bottom_price=fractal_bottom_price,
        fractal_bottom_time=fractal_bottom_time,
        too_late_patito_negro=too_late_patito_negro,
        too_late_brake_fractal_pauta_plana=too_late_brake_fractal_pauta_plana
    )

    print("\n=============== 📈 SUMMARY TRADE RESULT ================")
    summary_output_df = pd.DataFrame([trade_result])
    print(summary_output_df.T)
    print("===========================================================\n")
    if trade_result is None:
        print("⚠️ No se ejecutó ninguna operación. trade_result es None.")
        continue  # Salta a la siguiente fecha

    # ====================================================
    # GRAFICACIÓN DE DATOS 
    # ====================================================
    entry_time = trade_result['entry_trade_time']
    entry_price = trade_result['entry_trade_price']
    exit_time = trade_result['exit_trade_time']
    exit_price = trade_result['exit_trade_price']
    outcome = trade_result['outcome']
    profit= trade_result['profit']

    formated_titulo = START_DATE.strftime('%Y-%m-%d')
    titulo = f"SP500 Fecha entrada_{formated_titulo}_RESULTADO_{outcome}_{profit}_PUNTOS_Plotted on_{now_str}"

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
        entry_price,
        entry_time,
        exit_time,
        exit_price,
        fractal_bottoms_df
    )




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
