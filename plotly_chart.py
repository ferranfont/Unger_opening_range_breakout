import pandas as pd
import plotly.graph_objects as go
import os

def graficar_precio(df, titulo):
    if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        print("❌ DataFrame vacío o faltan columnas OHLC.")
        return

    os.makedirs("charts", exist_ok=True)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df.set_index('Date', inplace=True)

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    fig.update_layout(
        title=f"Velas Japonesas - {titulo}",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        xaxis_rangeslider_visible=False,
        template="plotly_white"
    )

    output_file = f'charts/{titulo}.html'
    fig.write_html(output_file)
    print(f"📁 Gráfico interactivo guardado como {output_file}")

    fig.show()
