def pauta_plana_study(after_open_df, END_TIME, first_breakout_pauta_plana_time, y0_value, y1_value, patito_negro_time, patito_negro):
    """
    Analyze the price behavior between the first breakout and the fractal breakout.
    """

    print("\n===== 🔍 Base after_open_df Info =====")
    print(f"Base DataFrame Start Time: {after_open_df.index.min()}")
    print(f"Base DataFrame End Time: {after_open_df.index.max()}")
    print(f"Base DataFrame Shape: {after_open_df.shape}")

    # Ensure correct time window (start ≤ index ≤ end)
    study_df = after_open_df[(after_open_df.index >= END_TIME) & (after_open_df.index <= first_breakout_pauta_plana_time)]

    print("\n===== 🔍 Filtered study_df (Segment) =====")
    print(study_df)
    print(f"Segment Shape: {study_df.shape}")

    if study_df.empty:
        print("⚠ Study period is empty. No analysis possible.")
        return None
    
    opening_range = y1_value - y0_value #opening rectangle range
    # Get minimum and maximum in the segment
    min_value = study_df['Low'].min()
    max_value = study_df['High'].max()

    # Calculate the min value in the mask or sub segment from green dot to green triangle
    
    if patito_negro_time is not None and first_breakout_pauta_plana_time is not None:
        mask = (after_open_df.index >= patito_negro_time) & (after_open_df.index <= first_breakout_pauta_plana_time)
        sub_df = after_open_df.loc[mask]

        if not sub_df.empty:
            min_after_fractal = sub_df['Low'].min()
            print(f"✅ Minimum value (Low) between fractal and entry: {min_after_fractal}")
        else:
            min_after_fractal = None
            print("⚠️ No data between fractal and entry to calculate minimum.")
    else:
        min_after_fractal = None
        print("⚠️ Fractal time or entry time is None; cannot compute minimum.")
   


    # Calculate patito_negro → min percentage
    patito_to_min_points = patito_negro - min_after_fractal
    patito_to_min_pct = (patito_to_min_points / patito_negro) * 100 if patito_negro != 0 else None

    # Check if y1 breakout (if max > y1_value)
    y1_breakout = False
    y1_to_max_points = 0
    if max_value > y1_value:
        y1_breakout = True
        y1_to_max_points = max_value - y1_value

    # Check if y0 breakdown (if min < y0_value)
    min_BO = False
    y0_to_min_points = 0
    if min_value < y0_value:
        min_BO = True
        y0_to_min_points = y0_value - min_value

    # Calculate pauta plana time range
    pauta_time_range = first_breakout_pauta_plana_time - END_TIME

    # Use start and end time from the base dataframe (not just filtered)
    segment_start_time = study_df.index.min()
    segment_end_time = study_df.index.max()

    # Return as dictionary for later use
    result = {
        'opening_range': opening_range,
        'pauta_plana_start_time': segment_start_time,        
        'pauta_plana_end_time': segment_end_time,
        'pauta_plana_duration': pauta_time_range,
        'BO_open_range_top': y1_breakout,
        'BO_open_range_top_to_max': y1_to_max_points,
        'BO_open_rage_bottom': min_BO,
        'BO_open_rage_bottom_to_min': y0_to_min_points,
        'pauta_plana_min': min_value,
        'pauta_plana_max': max_value,
        'retracment_from_fractal': patito_to_min_points,
        'PCT_retracment_from_fractal': patito_to_min_pct              
    }
    return result

