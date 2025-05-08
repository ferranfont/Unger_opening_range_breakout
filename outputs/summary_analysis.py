import pandas as pd
import os

# Define the path to the summary file
summary_file_path = os.path.join('outputs', 'summary_output_df.csv')

# Check if the file exists
if os.path.exists(summary_file_path):
    # Read the CSV file into a DataFrame
    summary_analysis = pd.read_csv(summary_file_path)
    print("✅ Summary file loaded successfully.")
    print(summary_analysis.head())  # Show first few rows
    print(summary_analysis.dtypes)
else:
    print(f"⚠️ Summary file not found at: {summary_file_path}")



total_profit = summary_analysis['profit'].sum()
print(f"💰 Total Profit: {total_profit}")

unique_outcomes = summary_analysis['outcome'].unique()
print("🎯 Unique 'outcome' values found:")
for outcome in unique_outcomes:
    print(f" - {outcome}")


# Total number of rows
total_rows = len(summary_analysis)
print(f"📊 Total rows in summary: {total_rows}")

# Check if 'outcome' column exists
if 'outcome' in summary_analysis.columns:
    # Count of each unique outcome
    outcome_counts = summary_analysis['outcome'].value_counts(dropna=False)
    print("\n🎯 Rows per 'outcome' value (including NaN):")
    print(outcome_counts)

    # Check for rows with missing or empty outcome
    missing_outcome_rows = summary_analysis[summary_analysis['outcome'].isna() | (summary_analysis['outcome'].astype(str).str.strip() == '')]
    num_missing = len(missing_outcome_rows)
    print(f"\n⚠️ Number of rows with missing or empty 'outcome': {num_missing}")

    if num_missing > 0:
        print("\nExample rows with missing or empty 'outcome':")
        print(missing_outcome_rows.head())
    else:
        print("⚠️ 'outcome' column not found in the summary file.")
else:
        print(f"⚠️ Summary file not found at: {summary_file_path}")

# Ensure 'profit' is numeric (in case it's read as string)
summary_analysis['profit'] = pd.to_numeric(summary_analysis['profit'], errors='coerce')

# Count rows where profit >= 0
profitable_trades = summary_analysis[summary_analysis['profit'] >= 0]
num_profitable = len(profitable_trades)
total_rows = len(summary_analysis)

print(f"📈 Number of trades with profit: {num_profitable}")
print(f"📊 Total trades: {total_rows}")
print(f"✅ Percentage profitable: {num_profitable / total_rows * 100:.2f}%")



if 'profit' in summary_analysis.columns and 'outcome' in summary_analysis.columns:
    # Ensure 'profit' is numeric (in case it's read as string)
    summary_analysis['profit'] = pd.to_numeric(summary_analysis['profit'], errors='coerce')

    # Filter rows with outcome == 'close_at_end' and profit >= 0
    filtered = summary_analysis[
        (summary_analysis['outcome'] == 'close_at_end') &
        (summary_analysis['profit'] >= 0)
    ]

    count_filtered = len(filtered)
    print(f"📊 Number of rows with outcome 'close_at_end' and profit: {count_filtered}")
else:
    print("⚠️ 'profit' or 'outcome' column not found in the summary file.")



valid_outcomes = ['close_at_end', 'stop_lost', 'target']
filtered = summary_analysis[summary_analysis['outcome'].isin(valid_outcomes)]

count_entries = len(filtered)
print(f"📊 Number of **real entries** (close_at_end + stop_lost + target): {count_entries}")


valid_outcomes = ['close_at_end', 'stop_lost', 'target']
filtered = summary_analysis[summary_analysis['outcome'].isin(valid_outcomes)]

count_profitable = len(filtered[filtered['profit'] >= 0])
print(f"💰 Number of real entries (close_at_end + stop_lost + target) with profit : {count_profitable}")


success_percentage = (count_profitable / count_entries) * 100
print(f"✅ Success percentage: {success_percentage:.2f}%")

profitable_rows = filtered[filtered['profit'] >= 0]
average_positive_profit = profitable_rows['profit'].mean()
print(f"💰 Average profit when profit ≥ 0: {average_positive_profit:.2f}")

# Filter rows with profit < 0
losing_rows = filtered[filtered['profit'] < 0]
average_negative_profit = losing_rows['profit'].mean()
print(f"📉 Average profit when profit < 0: {average_negative_profit:.2f}")


