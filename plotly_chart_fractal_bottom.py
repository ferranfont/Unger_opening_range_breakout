import pandas as pd
import plotly.graph_objects as go
import os

def graficar_precio(df, titulo, START_TIME, END_TIME, y0_value, y1_value, patito_negro_time, patito_negro, first_breakout_pauta_plana_time,  first_breakout_pauta_plana_price, entry_price, entry_time, exit_time, exit_price, fractal_bottoms_df=None): 

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

    # Add rectangle for the opening range
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

    # Add vertical line at END_TIME
    fig.add_shape(
        type="line",
        x0=END_TIME, x1=END_TIME,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color="blue", width=1),
        opacity=0.5
    )

    # Add fractal top marker (Patito Negro)
    fig.add_trace(go.Scatter(
        x=[patito_negro_time],
        y=[patito_negro],
        mode='markers',
        marker=dict(color='green', size=11, symbol='circle'),
        name='Fractal Patito Negro'
    ))

    # Add Pauta Plana point 
    fig.add_trace(go.Scatter(
        x=[first_breakout_pauta_plana_time],
        y=[first_breakout_pauta_plana_price],
        mode='markers',
        marker=dict(color='green', size=10, symbol='diamond'),
        name='Entry Point'
    ))

    # Add entry
    fig.add_trace(go.Scatter(
        x=[entry_time],
        y=[entry_price],
        mode='markers',
        marker=dict(color='green', size=15, symbol='triangle-up'),
        name='Entry Point'
    ))

    # Add exit point marker (target or stop)
    fig.add_trace(go.Scatter(
        x=[exit_time],
        y=[exit_price],
        mode='markers',
        marker=dict(color='red', size=15, symbol='triangle-down'),
        name='Exit Point'
    ))
    
    fig.add_trace(go.Scatter(
        x=[entry_time, exit_time],     # ✅ Tiempo en el eje X
        y=[entry_price, exit_price],   # ✅ Precio en el eje Y
        mode='lines',
        line=dict(color='gray', width=2, dash='dot'),
        name='Entry to Exit'
    ))

    # Add red dots for fractal bottoms if provided
    if fractal_bottoms_df is not None and not fractal_bottoms_df.empty:
        fig.add_trace(go.Scatter(
            x=fractal_bottoms_df.index,
            y=fractal_bottoms_df['Low'],
            mode='markers',
            marker=dict(color='red', size=12, symbol='circle'),
            name='Fractal Bottoms'
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
        width=1500,
        height=int(1500 * 0.45),
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
    print("🖥️  Gráfico mostrado en el navegador.")
