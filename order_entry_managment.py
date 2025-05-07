# GESTIÓN DE LA POSICIÓN, ENTRADA DE ORDENES, TARGET, STOP LOST, PAUTA PLANA
import pauta_plana_study as pp

def order_management_with_iterrows(
    after_open_df,
    y0_value,
    y1_value,
    opening_range,
    END_TIME,
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
    
    result = {
        "entry_trade_time": first_breakout_pauta_plana_time,
        "exit_trade_time": None,
        "trade_duration": None,
        "entry_trade_price": first_breakout_pauta_plana_price,
        "exit_trade_price": None,
        "outcome": None, #target, stop...
    }

    if not first_breakout_bool or not patito_negro_bool:
        print("⚠ No valid entry conditions met — exiting without trade.")
        return result

    if first_breakout_pauta_plana_price is None or first_breakout_pauta_plana_time is None:
        print("⚠ Missing breakout pauta plana price or time — skipping trade.")
        result['outcome'] = 'no_entry_conditions_met'
        return result

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

    after_entry_df = after_open_df[after_open_df.index >= first_breakout_pauta_plana_time]

    # Calculate MAE and MFE
    if not after_entry_df.empty:
        lowest_low = after_entry_df['Low'].min()
        highest_high = after_entry_df['High'].max()
        mae = first_breakout_pauta_plana_price - lowest_low  # adverse move
        mfe = highest_high - first_breakout_pauta_plana_price  # favorable move
    else:
        mae = None
        mfe = None

    # Iterate to determine exit
    for idx, row in after_entry_df.iterrows():
        high = row['High']
        low = row['Low']

        if high >= target_profit:
            trade_duration = idx - first_breakout_pauta_plana_time
            result['exit_trade_time'] = idx
            result['trade_duration'] = trade_duration
            result['exit_trade_price'] = target_profit
            result['outcome'] = 'target'
            break
        elif low <= stop_lost:
            trade_duration = idx - first_breakout_pauta_plana_time
            result['exit_trade_time'] = idx
            result['trade_duration'] = trade_duration
            result['exit_trade_price'] = stop_lost
            result['outcome'] = 'stop_lost'
            break

    if result['outcome'] is None and not after_entry_df.empty:
        trade_duration = idx - first_breakout_pauta_plana_time
        last_idx = after_entry_df.index[-1]
        last_close = after_entry_df.iloc[-1]['Close']
        result['exit_trade_time'] = last_idx
        result['trade_duration'] = trade_duration
        result['exit_trade_price'] = last_close
        result['outcome'] = 'close_at_end'

    # Calculate final profit
    if result['exit_trade_price'] is not None:
        result['profit'] = result['exit_trade_price'] - first_breakout_pauta_plana_price

    # Add MAE and MFE to result
    result['mae'] = mae
    result['mfe'] = mfe

    # Run pauta plana study
    pauta_plana_study_result = pp.pauta_plana_study(
        after_open_df=after_open_df,
        END_TIME=END_TIME,
        first_breakout_pauta_plana_time=first_breakout_pauta_plana_time,
        y0_value=y0_value,
        y1_value=y1_value,
        patito_negro=patito_negro
    )



    # Combine trade result and study result
    entry_output = {**result, **pauta_plana_study_result}

    return entry_output
