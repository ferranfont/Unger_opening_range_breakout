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
        close=df['Close'],
        increasing=dict(line=dict(color='black'), fillcolor='rgba(57, 255, 20, 0.5)'),  # Blue bullish candles, transparent fill
        decreasing=dict(line=dict(color='black'), fillcolor='red')    # Black bearish candles, solid fill
    )])

    # Adding a vertical line at 15:30 for each day in the chart
    unique_dates = pd.Series(df.index.date).unique()  # Convert to Series and use unique
    for day in unique_dates:
        vertical_line_time = pd.Timestamp(f'{day} 15:30:00')  # Create the timestamp for 15:30 of each day
        fig.add_shape(
            type="line",
            x0=vertical_line_time, x1=vertical_line_time,
            y0=0, y1=1,
            xref="x", yref="paper",
            line=dict(color="blue", width=1),  # Blue vertical line
            opacity=0.5  # Adjust opacity for better visibility 
        )

    fig.update_layout(
        title=f"Velas Japonesas - {titulo}",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        xaxis=dict(
            showgrid=False,
            showspikes=True,
            linecolor='darkgrey', 
            spikemode='across',
            spikesnap='cursor',
            spikecolor='grey',
            spikethickness=1,
            spikedash='dot',
            color='black'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            linecolor='darkgrey', 
            gridcolor='grey',  # Grey, discontinuous horizontal grid
            griddash='dot',
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikecolor='grey',
            spikethickness=1,
            spikedash='dot',
            color='black'
        ),
        xaxis_rangeslider_visible=False,
        width=1800,
        height=int(1800 * 0.45),  # Proportional height
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12, color="black"),
        title_font=dict(size=16, color="black"),
        xaxis_title_font=dict(size=14, color="black"),
        yaxis_title_font=dict(size=14, color="black"),
        legend=dict(font=dict(size=12, color="black")),
        paper_bgcolor="rgba(240, 240, 240, 0.6)",
        plot_bgcolor='rgba(255, 255, 255, 0.001)',
        dragmode="pan",
        spikedistance=-1
    )

    fig.update_traces(showlegend=False)

    # Enable scroll zoom with mouse wheel
    config = dict(scrollZoom=True)

    output_file = f'charts/{titulo}.html'
    fig.write_html(output_file, config=config)
    print(f"📁 Gráfico interactivo guardado como {output_file}")

    fig.show(config=config)
