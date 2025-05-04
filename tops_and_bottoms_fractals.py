import pandas as pd
import plotly.graph_objects as go

def find_first_strong_top(df, shifts=[1, 2], min_diff=0, titulo="Price Chart with First Fractal Top"): 
    series = df['High']
    condition = pd.Series(True, index=series.index)
    
    for s in shifts:
        condition &= (series > series.shift(s)) & (series > series.shift(-s))
    
    if min_diff > 0:
        for s in shifts:
            condition &= (series - series.shift(s)).abs() >= min_diff
            condition &= (series - series.shift(-s)).abs() >= min_diff
    
    matching_rows = df[condition]    

    # Start building the chart
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing=dict(line=dict(color='black'), fillcolor='rgba(57, 255, 20, 0.5)'),
        decreasing=dict(line=dict(color='black'), fillcolor='red'),
        hoverinfo='none',
        showlegend=False  # ← REMOVE trace 0 from legend
    ))

    # If a top is found, plot it as a green dot
    if not matching_rows.empty:
        first_top = matching_rows.iloc[0]
        top_time = matching_rows.index[0]
        top_value = first_top['High']

        fig.add_trace(go.Scatter(
            x=[top_time],
            y=[top_value],
            mode='markers',
            marker=dict(color='green', size=10, symbol='circle'),
            name='First Fractal Top'
        ))
    else:
        print("⚠ No top found — chart will show only candles.")

    fig.update_layout(
        title=titulo,
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis=dict(
            showgrid=False  # ← REMOVE vertical grid lines
        ),
        yaxis=dict(
            showgrid=True  # keep horizontal grid if desired
        ),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.5)',
            bordercolor='black',
            borderwidth=1,
            font=dict(size=10)
        ),
        xaxis_rangeslider_visible=False
    )

    fig.show()

    # Return the first matching row (or empty DataFrame)
    if not matching_rows.empty:
        return matching_rows.iloc[[0]]  # as DataFrame
    else:
        return pd.DataFrame(columns=df.columns)
