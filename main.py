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
ruta_completa = os.path.join(directorio, nombre_fichero)
df = pd.read_csv(ruta_completa)
print(df.head())
print(df.dtypes)


titulo = "Data "
chart.graficar_precio(df, titulo=f"{titulo}", columna='Close')
