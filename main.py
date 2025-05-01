# Sistema que lee y formatea data de Ninjatrader

from dotenv import load_dotenv
import pandas as pd
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

# Graficación del dataset
titulo = nombre_fichero.replace('.csv', '')
#chart.graficar_precio(df, titulo=titulo, columna='Close')
chart.graficar_precio(df, titulo=titulo)

