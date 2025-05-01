# archivo: grafico.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def graficar_precio(df, titulo, columna):
    if df.empty or columna not in df.columns:
        print("❌ DataFrame vacío o columna no encontrada.")
        return
    
    os.makedirs("charts", exist_ok=True)

    # Convertir Date a datetime (respetando zonas horarias)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df.set_index('Date', inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[columna], label="precios de cierre", linewidth=2)
    plt.title(f"Precios al cierre - {titulo}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.grid(axis="y")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'charts/{titulo}.png', bbox_inches='tight')
    print(f"📁 Gráfico guardado como charts/{titulo}.png")
    plt.show()


    
