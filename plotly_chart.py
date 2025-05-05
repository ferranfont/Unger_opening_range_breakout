import pandas as pd
import plotly.graph_objects as go
import os

def graficar_precio(df, titulo, START_DATE, END_DATE, START_TIME, END_TIME, y0_value, y1_value, patito_negro_time, patito_negro, target_filled_time, target_profit, first_breakout_pauta_plana_time, stop_lost_time, stop_lost, first_breakout_pauta_plana_price):
    if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        print("❌ DataFrame vacío o faltan columnas OHLC.")
        return

    os.makedirs("charts", exist_ok=True)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df.set_index('Date', inplace=True)
    df.index = df.index.tz_convert('Europe/Madrid')

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing=dict(line=dict(color='black'), fillcolor='rgba(57, 255, 20, 0.5)'),
        decreasing=dict(line=dict(color='black'), fillcolor='red'),
        hoverinfo='none'
    )])

    # Loop over each unique date
    unique_dates = pd.Series(df.index.date).unique()
    for day in unique_dates:
        # Build timezone-aware timestamps for the window
        #start_time = pd.Timestamp(f'{day} 15:00:00', tz='Europe/Madrid')
        #end_time = pd.Timestamp(f'{day} 15:30:00', tz='Europe/Madrid')
        # Add rectangle for the time range on this day
        fig.add_shape(
            type="rect",
            x0=START_TIME,
            x1=END_TIME,
            y0=y0_value,
            y1=y1_value,
            xref='x',
            yref='y',
            line=dict(color='lightblue', width=1),
            fillcolor='rgba(173, 216, 230, 0.5)',
            layer='below'
         )

        # Add vertical line at 15:30 on this day
        #vertical_line_time = pd.Timestamp(f'{day} 15:30:00', tz='Europe/Madrid')
        vertical_line_time = END_TIME
        fig.add_shape(
            type="line",
            x0=vertical_line_time, x1=vertical_line_time,
            y0=0, y1=1,
            xref="x", yref="paper",
            line=dict(color="blue", width=1),
            opacity=0.5
        )

        fig.add_trace(go.Scatter(
            x=[patito_negro_time],
            y=[patito_negro+0.5],
            mode='markers',
            marker=dict(color='green', size=11, symbol='circle'),
            name='First Fractal Top'
        ))

        fig.add_trace(go.Scatter(
            x=[first_breakout_pauta_plana_time],
            y=[first_breakout_pauta_plana_price+0.5],
            mode='markers',
            marker=dict(color='green', size=17, symbol='triangle-up'),
            name='First Fractal Top'
        ))

        fig.add_trace(go.Scatter(
            x=[target_filled_time],
            y=[target_profit],
            mode='markers',
            marker=dict(color='red', size=17, symbol='triangle-down'),
            name='First Fractal Top'
        ))

        fig.add_trace(go.Scatter(
            x=[stop_lost_time],
            y=[stop_lost],
            mode='markers',
            marker=dict(color='red', size=17, symbol='triangle-down'),
            name='First Fractal Top'
        ))
        
    fig.update_layout(
        title=f"{titulo}",
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
            color='black',

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
            color='black',
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
    print(f"\n📁 Gráfico interactivo guardado como {output_file}")

    fig.show(config=config)
    print("✅ Gráfico mostrado en el navegador.")
    

