# archivo: grafico.py

import matplotlib.pyplot as plt
import os

def graficar_precio(df, titulo, columna):
    if df.empty or columna not in df.columns:
        print("❌ DataFrame vacío o columna no encontrada.")
        return
    
    os.makedirs("charts", exist_ok=True)    

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[columna], label="precios de cierre", linewidth=2)
    plt.title(titulo)
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.grid(axis="y")  # Solo líneas horizontales (eje Y)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'charts/{titulo}.png', bbox_inches='tight')
    print(f"📁 Gráfico guardado")
    plt.show()
    
