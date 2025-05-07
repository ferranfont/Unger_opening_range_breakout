def order_management_with_iterrows(
    after_open_df,
    y0_value,
    y1_value,
    opening_range,
    patito_negro,
    first_breakout_bool,
    first_breakout_time,
    first_breakout_price,
    first_breakdown_bool,
    first_breakdown_time,
    first_breakdown_price,
    patito_negro_bool,
    patito_negro_time,
    first_breakout_pauta_plana_price,
    first_breakout_pauta_plana_time
):

    # Initialize results
    result = {
        "entry_time": first_breakout_pauta_plana_time,
        "entry_price": first_breakout_pauta_plana_price,
        "exit_time": None,
        "exit_price": None,
        "outcome": None  # 'target', 'stop', 'close_at_end'
    }

    # Check entry conditions
    if not first_breakout_bool or not patito_negro_bool:
        print("⚠ No valid entry conditions met — exiting without trade.")
        return result

    # Check for missing critical inputs
    if first_breakout_pauta_plana_price is None or first_breakout_pauta_plana_time is None:
        print("⚠ Missing breakout pauta plana price or time — skipping trade.")
        result['outcome'] = 'no_entry_conditions_met'
        return result

    # Define stop and target levels
    multiplier = 18
    stop_tolerance = 2
    stop_lost = y0_value - stop_tolerance
    target_profit = first_breakout_pauta_plana_price + opening_range * multiplier

    print("\n===== 🚀 TRADE INITIATED =====")
    print(f"Entry Time: {first_breakout_pauta_plana_time}")
    print(f"Entry Price: {first_breakout_pauta_plana_price}")
    print(f"Target Price: {target_profit}")
    print(f"Stop Price: {stop_lost}")
    print("============================\n")

    # Filter only rows after the entry time
    after_entry_df = after_open_df[after_open_df.index >= first_breakout_pauta_plana_time]

    # Iterate through DataFrame chronologically after entry
    for idx, row in after_entry_df.iterrows():
        high = row['High']
        low = row['Low']

        if high >= target_profit:
            result['exit_time'] = idx
            result['exit_price'] = target_profit
            result['outcome'] = 'target'
            print(f"✅ Target hit at {idx} with price {high}")
            break
        elif low <= stop_lost:
            result['exit_time'] = idx
            result['exit_price'] = stop_lost
            result['outcome'] = 'stop'
            print(f"❌ Stop hit at {idx} with price {low}")
            break

    # If neither target nor stop was hit, close at last candle
    if result['outcome'] is None:
        last_idx = after_entry_df.index[-1]
        last_close = after_entry_df.iloc[-1]['Close']
        result['exit_time'] = last_idx
        result['exit_price'] = last_close
        result['outcome'] = 'close_at_end'
        print(f"🔚 No target or stop hit — closing at end of session: {last_idx} with price {last_close}")

    return result

