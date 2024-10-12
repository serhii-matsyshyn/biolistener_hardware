import pandas as pd
import glob


def merge_bom_files(bom_files, output_file):
    # List to store all DataFrames
    all_dataframes = []

    for file in bom_files:
        # Read each CSV file into a DataFrame
        df = pd.read_csv(file, encoding='utf-16', sep='\t', quotechar='"',)
        # Drop the 'ID' column as it's unimportant
        df = df.drop(columns=['ID', 'Designator', 'Price'])
        all_dataframes.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    # Convert 'Quantity' to numeric in case it's read as a string
    combined_df['Quantity'] = pd.to_numeric(combined_df['Quantity'], errors='coerce')

    # Group by columns that must match exactly and sum the 'Quantity'
    grouped_df = combined_df.groupby(
        ['Name', 'Footprint', 'Manufacturer Part', 'Manufacturer', 'Supplier', 'Supplier Part'],
        as_index=False
    ).agg({'Quantity': 'sum'})

    # Write the result to the output CSV file
    grouped_df.to_csv(output_file, index=False, sep='\t', quotechar='"',)
    print(f"Merged BOM saved to {output_file}")


# Example usage
if __name__ == "__main__":
    # Get all BOM .csv files from the current directory (or modify the path as needed)
    bom_files = glob.glob("BOM_*.csv")  # adjust the pattern as per your file names
    output_file = "out/merged_bom.csv"
    merge_bom_files(bom_files, output_file)
