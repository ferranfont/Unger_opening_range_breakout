# Este código devuelve un suelo fuerte que es buscado tras la rotura
import pandas as pd

def find_all_strong_bottoms(df, shifts=[1, 2], min_diff=0):
    """
    Detect all strong fractal bottoms (local minima) in the DataFrame.
    Marks points where Low is lower than surrounding values (shifts).

    Parameters:
        df (pd.DataFrame): DataFrame with 'Low' column.
        shifts (list): list of shift values to check.
        min_diff (float): minimum difference to consider significant.

    Returns:
        pd.DataFrame: DataFrame with all detected fractal bottoms.
    """
    series = df['Low']
    condition = pd.Series(True, index=series.index)

    for s in shifts:
        condition &= (series < series.shift(s)) & (series < series.shift(-s))

    if min_diff > 0:
        for s in shifts:
            condition &= (series - series.shift(s)).abs() >= min_diff
            condition &= (series - series.shift(-s)).abs() >= min_diff

    matching_rows = df[condition].iloc[[0]]
    fractal_bottom_bool = True
    return matching_rows, fractal_bottom_bool if not matching_rows.empty else pd.DataFrame(columns=df.columns)

