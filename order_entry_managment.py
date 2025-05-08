# GESTIÓN DE LA POSICIÓN, ENTRADA DE ORDENES, TARGET, STOP LOST, PAUTA PLANA
import pauta_plana_study as pp
import pandas as pd
import os

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
    first_breakout_pauta_plana_time,
    too_late_patito_negro,
    too_late_brake_fractal_pauta_plana
):

    result = {
        "entry_trade_time": first_breakout_pauta_plana_time,
        "exit_trade_time": None,
        "trade_duration": None,
        "entry_trade_price": first_breakout_pauta_plana_price,
        "exit_trade_price": None,
        "profit": None,
        "outcome": None, # Label: target, stop...
    }

    if not first_breakout_bool or not patito_negro_bool:
        print("☢️  No valid entry conditions met — exiting without entry.")
        return result

    if first_breakout_pauta_plana_price is None or first_breakout_pauta_plana_time is None:
        print("☢️  Missing breakout pauta plana price or time — skipping entry.")
        result['outcome'] = 'no_entry_conditions_met'
        return result
    
    # no operamos si el fractal o patito negro es realizado muy tarde
    if patito_negro_time > too_late_patito_negro:
        print("☢️  Patito Negro breakout time is too late — skipping entry.")
        result['outcome'] = 'no_entry'
        return result
    
    # no operamos si la entrada es muy tarde
    if first_breakout_pauta_plana_time is None or first_breakout_pauta_plana_time > too_late_brake_fractal_pauta_plana:
        print("☢️  Fractal Break Out too late - skipping entry")
        result['outcome'] = 'no_entry_due_to_late_time'
        return result


    multiplier = 3
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

    # Calculate MAE (Maximum Adverse Excursion) ensuring stop_lost is set
    if stop_lost is None:
        raise ValueError("The variable 'stop_lost' (stop loss price) is not set before MAE calculation.")

    max_profit_so_far = 0
    max_drawdown_so_far = 0
    max_favorable_so_far = 0  # MFE tracking

    entry_price = first_breakout_pauta_plana_price

    for idx, row in after_open_df.iterrows():
        current_high = row['High']
        current_low = row['Low']

        # Assuming long position
        current_profit = current_high - entry_price

        # Update maximum profit (MFE)
        if current_profit > max_favorable_so_far:
            max_favorable_so_far = current_profit

        # Update max profit for drawdown calculation
        if current_profit > max_profit_so_far:
            max_profit_so_far = current_profit

        # Calculate drawdown (MAE)
        drawdown = max_profit_so_far - (current_high - entry_price)

        # Ensure we don't exceed the stop loss level
        potential_drawdown = max(entry_price - stop_lost, drawdown)
        if potential_drawdown > max_drawdown_so_far:
            max_drawdown_so_far = potential_drawdown

    # Final metrics
    mae_points = max_drawdown_so_far
    mae_pct = (mae_points / entry_price) * 100 if entry_price else 0
    mfe_points = max_favorable_so_far

    # Add to result dictionary
    result['MAE_points'] = mae_points
    result['MAE_pct'] = mae_pct
    result['MFE_points'] = mfe_points

    print(f"📉 Maximum Adverse Excursion (MAE): {mae_points:.2f} points ({mae_pct:.2f}%)")
    print(f"📈 Maximum Favorable Excursion (MFE): {mfe_points:.2f} points")


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

    # Run pauta plana study
    pauta_plana_study_result = pp.pauta_plana_study(
        after_open_df,
        END_TIME,
        first_breakout_pauta_plana_time,
        y0_value,
        y1_value,
        patito_negro_time,
        patito_negro
    )


    # Combine trade result and study result
    entry_output = {**result, **pauta_plana_study_result}

    return entry_output
