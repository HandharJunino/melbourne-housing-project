import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

def load_to_postgres(csv_path, table_name, db_url):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file at {csv_path} is empty.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV: {e}")
        return

    try:
        engine = create_engine(db_url)
        # Test connection (optional but good practice)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Loaded data into {table_name} table successfully.")
    except Exception as e:
        print(f"Error loading data to PostgreSQL: {e}")
        print("Please check your database URL, credentials, and ensure the PostgreSQL server is running.")

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Build absolute path to the cleaned CSV file
    csv_path = os.path.join(project_dir, 'data', 'cleaned', 'cleaned_data.csv')
    
    DATABASE_URL = os.getenv('DATABASE_URL')
    load_to_postgres(csv_path, 'melb_housing', DATABASE_URL)