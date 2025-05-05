# Este código devuelve el primer máximo fuerte en un DataFrame de pandas.

import pandas as pd

def find_first_strong_top(df, y0_value, y1_value, shifts=[1, 2], min_diff=0): 
    series = df['High']
    condition = pd.Series(True, index=series.index)
    
    for s in shifts:
        condition &= (series > series.shift(s)) & (series > series.shift(-s))
    
    if min_diff > 0:
        for s in shifts:
            condition &= (series - series.shift(s)).abs() >= min_diff
            condition &= (series - series.shift(-s)).abs() >= min_diff

    condition &= (series > y1_value)

    matching_rows = df[condition]    

    # Return the first matching row (or empty DataFrame)
    if not matching_rows.empty:
        return matching_rows.iloc[[0]]  # as DataFrame
    else:
        return pd.DataFrame(columns=df.columns)
