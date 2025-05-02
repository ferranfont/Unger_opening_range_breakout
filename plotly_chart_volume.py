import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def graficar_precio(df, titulo):
    if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volumen']):
        print("❌ DataFrame vacío o faltan columnas OHLC o Volumen.")
        return

    os.makedirs("charts", exist_ok=True)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df.set_index('Date', inplace=True)
    df.index = df.index.tz_convert('Europe/Madrid')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.85, 0.15], vertical_spacing=0.02)

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing=dict(line=dict(color='black'), fillcolor='rgba(57, 255, 20, 0.5)'),
        decreasing=dict(line=dict(color='black'), fillcolor='red'),
        hoverinfo='none'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Volumen'],
        marker_color='blue',
        opacity=0.5,
        hoverinfo='skip'
    ), row=2, col=1)

    # Add rectangles and vertical lines per day
    unique_dates = pd.Series(df.index.date).unique()
    for day in unique_dates:
        start_time = pd.Timestamp(f'{day} 15:00:00', tz='Europe/Madrid')
        end_time = pd.Timestamp(f'{day} 15:30:00', tz='Europe/Madrid')

        window_df = df[(df.index >= start_time) & (df.index <= end_time)]
        if not window_df.empty:
            y0_value = window_df['Low'].min()
            y1_value = window_df['High'].max()

            fig.add_shape(
                type="rect",
                x0=start_time,
                x1=end_time,
                y0=y0_value,
                y1=y1_value,
                xref='x',
                yref='y',
                line=dict(color='lightblue', width=1),
                fillcolor='rgba(173, 216, 230, 0.5)',
                layer='below',
                row=1, col=1
            )

        vertical_line_time = pd.Timestamp(f'{day} 15:30:00', tz='Europe/Madrid')
        fig.add_shape(
            type="line",
            x0=vertical_line_time, x1=vertical_line_time,
            y0=0, y1=1,
            xref="x", yref="paper",
            line=dict(color="blue", width=1),
            opacity=0.5
        )

    fig.update_layout(
        title=f"Velas Japonesas - {titulo}",
        xaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikecolor='grey',
            spikethickness=1,
            linecolor='darkgrey',
            color='black'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            linecolor='darkgrey',
            gridcolor='grey',
            griddash='dot',
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikecolor='grey',
            spikethickness=1,
            color='black'
        ),
        xaxis2=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikecolor='grey',
            spikethickness=1,
            linecolor='darkgrey',
            color='black'
        ),
        yaxis2=dict(
            showgrid=True,
            gridwidth=1,
            linecolor='darkgrey',
            gridcolor='grey',
            griddash='dot',
            color='black'
        ),
        xaxis_rangeslider_visible=False,
        width=1800,
        height=int(1800 * 0.45),
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

    config = dict(scrollZoom=True)

    output_file = f'charts/{titulo}.html'
    fig.write_html(output_file, config=config)
    print(f"📁 Gráfico interactivo guardado como {output_file}")

    fig.show(config=config)