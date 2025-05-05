# Con este código se gestiona las posiciones de compra, venta, stops y targets
def order_management(after_open_df, y0_value, y1_value, opening_range, patito_negro, first_breakout_pauta_plana_price, first_breakout_pauta_plana_time):
    target_filled_time = None
    target_profit = None
    stop_lost_time =None
    stop_lost = None
    
    # definicion del Stop Lost
    multiplier = 1
    stop_tolerance = 2
    stop_lost = y0_value - stop_tolerance
    target_profit = first_breakout_pauta_plana_price + opening_range * multiplier

    print("\n===================================================================================================")
    print(f"⚡⚡⚡ Entrada -Compra- al mercado a las: {first_breakout_pauta_plana_time} en el precio {first_breakout_pauta_plana_price} ⚡⚡⚡")
    print(f"        🎯 Target at {target_profit} & 🛑 Stop at {stop_lost}")
    print("===================================================================================================")

    # primera fila que llega al target

    filtered_target = after_open_df[after_open_df['High'] > target_profit]
    filtered_stop = after_open_df[after_open_df['Low'] < stop_lost]
    if not filtered_target.empty:
        target_filled_time = filtered_target.index[0]
        print(f"✅ Target alcanzado a las {target_filled_time} en el precio {target_profit}")
    else:
        stop_lost_time = filtered_stop.index[0] 
        print(f"❌ Stop_Lost alcanzado a las {stop_lost_time} en el precio {stop_lost}")


    return target_filled_time, target_profit, stop_lost_time, stop_lost
    # primera fila que llega al stop lost


