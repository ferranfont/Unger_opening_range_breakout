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
    fractal_bottom_bool,
    fractal_bottom_price,
    fractal_bottom_time,
    too_late_patito_negro,
    too_late_brake_fractal_pauta_plana

):
    print("Condiciones de Mercado: ")
    print(f"Rotura Superior Cuadradito: {first_breakout_bool}\nRotura Inferior Cuadradito: {first_breakdown_bool}\nFractal Top: {patito_negro_bool}\nFractal Bottom: {fractal_bottom_bool}\n")
    result = None    
    entry = False  # Default

    if first_breakout_bool and fractal_bottom_bool: # AQUÍ SE INDICA EL ALGORITMO DE ENTRADA AL MERCADO: EN ESTE CASO- ROTURA CUADRADITO +  FRACTAL BOTTOM TRAS LA ROTUA
        try:
            position = after_open_df.index.get_loc(fractal_bottom_time)
            if position + 2 < len(after_open_df):
                entry_time = after_open_df.index[position + 2]
                entry_price = after_open_df.iloc[position + 2]['Close']
                entry = True  # Set flag
        except KeyError:
            print("❌ fractal_bottom_time not found in index.")

        multiplier = 2
        mediana = opening_range/2
        stop_tolerance = mediana
        stop_lost = entry_price - stop_tolerance
        #target_profit = fractal_bottom_price + 10 * multiplier
        target_profit = entry_price + mediana * multiplier


        print("\n======== 🚀 TRADE INITIATED ========")
        print(f"✅ Entry signal: True")
        print(f"🕒 Entry Time: {entry_time}")
        print(f"💲 Entry Price: {entry_price}")
        print(f"💲 Target Price: {target_profit}")
        print(f"🛑 Stop Price: {stop_lost}")
        print("==================================\n")

        result = {
            "entry_trade_time": entry_time,
            "exit_trade_time": None,
            "trade_duration": None,
            "entry_trade_price": entry_price,
            "exit_trade_price": None,
            "profit": None,
            "outcome": None,  # 'target', 'stop_lost', etc.
        }

        # Iterate to determine exit
        for idx, row in after_open_df[after_open_df.index >= entry_time].iterrows():
    
            high = row['High']
            low = row['Low']

            if high >= target_profit:
                trade_duration = idx - entry_time
                result['exit_trade_time'] = idx
                result['trade_duration'] = trade_duration
                result['exit_trade_price'] = target_profit
                result['outcome'] = 'target'
                break
            elif low <= stop_lost:
                trade_duration = idx - entry_time
                result['exit_trade_time'] = idx
                result['trade_duration'] = trade_duration
                result['exit_trade_price'] = stop_lost
                result['outcome'] = 'stop_lost'
                break

        if result['outcome'] is None and not after_open_df.empty:
            trade_duration = idx - entry_time
            last_idx = after_open_df.index[-1]
            last_close = after_open_df.iloc[-1]['Close']
            result['exit_trade_time'] = last_idx
            result['trade_duration'] = trade_duration
            result['exit_trade_price'] = last_close
            result['outcome'] = 'close_at_end'

        # Calculate final profit
        if result['exit_trade_price'] is not None:
            result['profit'] = result['exit_trade_price'] - entry_price


        # ================================
        # 📊 CÁLCULO DE MFE Y MAE
        # ================================
        max_favorable_so_far = 0
        max_drawdown_so_far = 0
        max_profit_so_far = 0  # para calcular drawdown
        stop_lost = entry_price - 4 if stop_lost is None else stop_lost  # seguridad

        for idx, row in after_open_df[after_open_df.index >= entry_time].iterrows():
            current_high = row['High']
            current_low = row['Low']

            # MFE: excursión máxima a favor
            current_profit = current_high - entry_price
            if current_profit > max_favorable_so_far:
                max_favorable_so_far = current_profit

            # MAE: excursión máxima en contra
            current_drawdown = entry_price - current_low
            if current_drawdown > max_drawdown_so_far:
                max_drawdown_so_far = current_drawdown

        # Añadir a resultados
        result['MAE_points'] = max_drawdown_so_far
        result['MAE_pct'] = (max_drawdown_so_far / entry_price) * 100 if entry_price else 0
        result['MFE_points'] = max_favorable_so_far

        print(f"📉 Maximum Adverse Excursion (MAE): {result['MAE_points']:.2f} puntos ({result['MAE_pct']:.2f}%)")
        print(f"📈 Maximum Favorable Excursion (MFE): {result['MFE_points']:.2f} puntos\n")

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

    

        '''

        # No se entra porque no hay rotura del cuadradito
        if not first_breakout_bool or not patito_negro_bool:
            print("☢️  No valid entry conditions met — exiting without entry.")
            return result

        # No se entra porque no hay rotura de la pauta plana o la rotura es demasiado tarde en el tiempo
        if first_breakout_pauta_plana_price is None or first_breakout_pauta_plana_time is None:
            print("☢️  Missing breakout pauta plana price or time — skipping entry.")
            result['outcome'] = 'no_entry_conditions_met'
            return result
        
        # Filtro asegurarse de que hay un fractal/rotura del cuadradito antes de buscar una entrada
        if patito_negro_time > too_late_patito_negro:
            print("☢️  Patito Negro breakout time is too late — skipping entry.")
            result['outcome'] = 'no_entry'
            return result
        
        # No se entra si la rotura del fractal/patito negro se produce muy tarde
        if first_breakout_pauta_plana_time is None or first_breakout_pauta_plana_time > too_late_brake_fractal_pauta_plana:
            print("☢️  Fractal Break Out too late - skipping entry")
            result['outcome'] = 'no_entry_due_to_late_time'
            return result
        

      

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
        '''
