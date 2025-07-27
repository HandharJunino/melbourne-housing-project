import pandas as pd
import numpy as np
import os

def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # convert the dates to datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%d/%m/%Y')

    # drop rows with invalid dates
    df.dropna(subset=['Date'], inplace=True)

    # --- handling missing values ---
    # flag missing prices
    df['missing_Price'] = df['Price'].isnull().astype(int)
    # drop rows with missing prices
    #df.dropna(subset=['Price'], inplace=True)

    # impute numerical columns with their median
    for col in ['Landsize', 'Car', 'Bathroom', 'Bedroom2', 'Lattitude', 'Longtitude', 'Propertycount', 'Distance', 'Postcode']:
        if col in df.columns and df[col].isnull().any():
            median_value = df[col].median()
            df[col].fillna(median_value, inplace=True)

    # Impute categorical columns with their mode (for Regionname, CouncilArea)
    for col in ['Regionname', 'CouncilArea']:
        if col in df.columns and df[col].isnull().any():
            df[col].fillna(df[col].mode()[0], inplace=True)

    # --- Correct Data Types ---
    # Convert appropriate columns to integer types after handling NaNs
    for col in ['Postcode', 'Bedroom2', 'Bathroom', 'Car', 'Rooms', 'Propertycount']:
        if col in df.columns:
            # Convert to Int64 to handle potential NaN temporarily if not fully imputed
            # Or convert to int directly if no NaNs are expected after imputation
            df[col] = df[col].astype('Int64') # Using 'Int64' to allow for NaNs if any remain, otherwise 'int'

    # --- handle outliers ---
    # Remove outliers in Price using IQR method
    Q1 = df['Price'].quantile(0.25)
    Q3 = df['Price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    #df = df[(df['Price'] >= lower_bound) & (df['Price'] <= upper_bound)]

    # remove landsize outliers
    upper_landsize = df['Landsize'].quantile(0.995) # using 99.5th percentile to remove extreme outliers
    lower_landsize = 0
    df = df[(df['Landsize'] <= upper_landsize) & (df['Landsize'] >= lower_landsize)]

    # feature engineering
    # Extract year and month from the Date column
    df['SaleYear'] = df['Date'].dt.year
    df['SaleMonth'] = df['Date'].dt.month
    df['HouseAge'] = df['SaleYear'] - df['YearBuilt']
    df['HouseAge'] = df['HouseAge'].fillna(df['HouseAge'].median())

    # RoomsPerBathroom: df['Rooms'] / (df['Bathroom'] + 1)
    df['RoomsPerBathroom'] = df['Rooms'] / (df['Bathroom'] + 1)
    df['RoomsPerBathroom'] = df['RoomsPerBathroom'].round(2) # Round for clarity

    # LandsizePerRoom: df['Landsize'] / (df['Rooms'] + 1)
    df['LandsizePerRoom'] = df['Landsize'] / (df['Rooms'] + 1)
    df['LandsizePerRoom'] = df['LandsizePerRoom'].round(2) # Round for clarity

    # BuildingDensity: df['BuildingArea'] / (df['Landsize'] + 1)
    # Adding a small epsilon (1e-6) to the denominator to prevent division by zero if Landsize is 0.
    df['BuildingDensity'] = df['BuildingArea'] / (df['Landsize'] + 1e-6)
    df['BuildingDensity'].replace([np.inf, -np.inf], np.nan, inplace=True) # Replace any resulting inf with NaN
    df['BuildingDensity'].fillna(0, inplace=True) # Fill any NaNs (e.g., if BuildingArea was 0 and Landsize was 0)
    df['BuildingDensity'] = df['BuildingDensity'].round(4) # Round for clarity, often smaller values

    # PricePerSqm: df['Price'] / (df['Landsize'] + 1)
    # Adding a small epsilon (1e-6) to the denominator to prevent division by zero if Landsize is 0.
    df['PricePerSqm'] = df['Price'] / (df['Landsize'] + 1e-6)
    df['PricePerSqm'].replace([np.inf, -np.inf], np.nan, inplace=True) # Replace any resulting inf with NaN
    df['PricePerSqm'].fillna(0, inplace=True) # Fill any NaNs (e.g., if Landsize was 0)
    df['PricePerSqm'] = df['PricePerSqm'].round(2) # Round to 2dp for monetary value

    # drop rows with missing dates
    df.dropna(subset=['Date'], inplace=True)

    # drop  building area and yearbuilt due to many missing values
    df.drop(columns=['BuildingArea', 'YearBuilt'], inplace=True)

    # save the transformed data
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    input_path = os.path.join(project_dir, 'data', 'raw', 'Melbourne_housing_FULL.csv')
    output_path = os.path.join(project_dir, 'data', 'cleaned', 'cleaned_data.csv')
    
    # Ensure the cleaned directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    clean_data(input_path, output_path)
    print("Data cleaning complete. Cleaned data saved to:", output_path)
