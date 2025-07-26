import pandas as pd
import glob
import os

path = "/Users/niharikarawat/Downloads/California airbnb/"
csv_files = glob.glob(os.path.join(path, "*.csv"))

df_list = []
for file in csv_files:
    try:
        df = pd.read_csv(file)
        city_name = os.path.basename(file).replace(".csv", "")
        df['city'] = city_name
        df_list.append(df)
        print(f"Successfully loaded {file} with {len(df)} rows")
    except Exception as e:
        print(f"Error loading {file}: {e}")

combined_df = pd.concat(df_list, ignore_index=True)

print(f"Combined dataset shape: {combined_df.shape}")
print("\nFirst few rows:")
print(combined_df.head())
print(f"\nCities in dataset: {combined_df['city'].unique()}")

combined_df.to_csv("B-merged_airbnb.csv", index=False)
print("Merged CSV saved as B-merged_airbnb.csv")
