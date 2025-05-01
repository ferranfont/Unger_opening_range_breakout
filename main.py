# Sistema que lee y formatea data de Ninjatrader

from dotenv import load_dotenv
import pandas as pd
import chart
import config
import os
load_dotenv()

import os
import pandas as pd

# Separar directorio y nombre del archivo
directorio = '../DATA'
nombre_fichero = 'export_es_2015_formatted.csv'
#nombre_fichero = 'export_NQ_2015_formatted.csv'
#nombre_fichero = 'export_6E_2015_formatted.csv'
#nombre_fichero = 'export_YM_2015_formatted.csv'
#nombre_fichero = 'export_GC_2015_formatted.csv'


ruta_completa = os.path.join(directorio, nombre_fichero)

# Leer CSV
df = pd.read_csv(ruta_completa)

# Mostrar preview
print(df.head())
print(df.dtypes)

# Título para gráfico
titulo = nombre_fichero.replace('.csv', '')

# Graficar
chart.graficar_precio(df, titulo=titulo, columna='Close')