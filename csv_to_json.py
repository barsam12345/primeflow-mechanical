import pandas as pd, sys, json, pathlib

# Look for the Excel file in the Downloads folder
excel_file_name = "Exercise-Database.xlsx" # Assuming this is the name from the screenshot
downloads_path = pathlib.Path.home() / "Downloads"
excel_path = downloads_path / excel_file_name

# Check if the Excel file exists
if not excel_path.exists():
    # Fallback to CSV in the current directory if Excel is not found (as originally designed)
    # Or, if the user *did* save as CSV and moved it.
    print(f"Warning: Excel file not found at {excel_path}. Trying 'Exercise-Database.csv' in current directory.", file=sys.stderr)
    csv_path_local = pathlib.Path("Exercise-Database.csv")
    if not csv_path_local.exists():
        print(f"Error: Neither {excel_path} nor {csv_path_local} found. Please ensure your data file is correctly named and placed.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(csv_path_local)
    output_json_name = "exercises.json" # Consistent with HTML
    json_path = pathlib.Path(output_json_name)
else:
    print(f"Reading Excel file from: {excel_path}")
    df = pd.read_excel(excel_path) # Reading .xlsx directly
    output_json_name = "exercises.json" # Name expected by index.html and client.html
    json_path = pathlib.Path(output_json_name) # Save in the script's directory (workspace root)


df.fillna("", inplace=True)           # kill NaNs
json_path.write_text(df.to_json(orient="records"), encoding="utf‑8")
print("Wrote", json_path) 