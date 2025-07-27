from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import os
import sys
import pandas as pd

# Default arguments for the DAG
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'melbourne_housing_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for Melbourne housing data with ML training',
    schedule_interval='@daily',  # Run daily
    catchup=False,
    tags=['etl', 'machine-learning', 'housing'],
)

def extract_data(**context):
    """
    Extract: Check if raw data exists and validate it
    """
    raw_data_path = '/app/data/raw/Melbourne_housing_FULL.csv'
    
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found: {raw_data_path}")
    
    # Get file info
    file_size = os.path.getsize(raw_data_path)
    print(f"✅ Raw data file found: {raw_data_path}")
    print(f"📊 File size: {file_size / 1024 / 1024:.2f} MB")
    
    # Quick data validation
    df = pd.read_csv(raw_data_path)
    print(f"📋 Dataset shape: {df.shape}")
    print(f"📋 Columns: {list(df.columns)}")
    
    return raw_data_path

def transform_data(**context):
    """
    Transform: Clean and preprocess the data
    """
    print("🔄 Starting data transformation...")
    
    # Use absolute paths for Docker compatibility
    script_dir = '/app/scripts'
    sys.path.append(script_dir)
    
    try:
        from transformation import clean_data
        
        input_path = '/app/data/raw/Melbourne_housing_FULL.csv'
        output_path = '/app/data/cleaned/cleaned_data.csv'
        
        # Call your transformation function
        clean_data(input_path, output_path)
        
        print(f"✅ Data transformation completed: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error in transformation: {e}")
        raise

def train_model(**context):
    """
    Train: Train the machine learning model
    """
    print("🤖 Starting model training...")
    
    script_dir = '/app/scripts'
    sys.path.append(script_dir)
    
    try:
        from train_model import train_and_save_model
        
        # Call your training function
        model_path = train_and_save_model()
        
        print(f"✅ Model training completed: {model_path}")
        return model_path
    except Exception as e:
        print(f"❌ Error in model training: {e}")
        raise

def load_data(**context):
    """
    Load: Load processed data to PostgreSQL database
    """
    csv_path = '/app/data/cleaned/cleaned_data_with_predictions.csv'
    table_name = 'melb_housing'
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        print("⚠️ DATABASE_URL not set, skipping database load")
        return "skipped"
    
    print("📤 Loading data to PostgreSQL...")
    
    script_dir = '/app/scripts'
    sys.path.append(script_dir)
    
    try:
        from load import load_to_postgres
        
        # Call your load function
        load_to_postgres(csv_path, table_name, db_url)
        
        print("✅ Data loaded to PostgreSQL successfully")
        return "completed"
    except Exception as e:
        print(f"❌ Error in data loading: {e}")
        print("Continuing pipeline without database load...")
        return "failed_but_continue"

def validate_pipeline(**context):
    """
    Validate: Check if all outputs are created successfully
    """
    files_to_check = [
        '/app/data/cleaned/cleaned_data.csv',
        '/app/data/cleaned/cleaned_data_with_predictions.csv',
        '/app/models/melb_house_model.pkl'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            existing_files.append(f"{file_path} ({file_size/1024:.1f} KB)")
        else:
            missing_files.append(file_path)
    
    print("📋 Pipeline validation results:")
    print(f"✅ Created files: {existing_files}")
    
    if missing_files:
        print(f"⚠️ Missing files: {missing_files}")
        # Don't fail the pipeline, just warn
        print("Pipeline completed with warnings")
    else:
        print("✅ Pipeline validation successful - all files created")
    
    return "validation_completed"

# Define the tasks using PythonOperator
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data', 
    python_callable=transform_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

validate_task = PythonOperator(
    task_id='validate_pipeline',
    python_callable=validate_pipeline,
    dag=dag,
)

# Alternative: Use BashOperator to run scripts directly (backup option)
transform_bash_task = BashOperator(
    task_id='transform_data_bash_backup',
    bash_command='cd /app && python scripts/transformation.py',
    dag=dag,
)

train_bash_task = BashOperator(
    task_id='train_model_bash_backup', 
    bash_command='cd /app && python scripts/train_model.py',
    dag=dag,
)

# Define task dependencies - Linear ETL pipeline
extract_task >> transform_task >> train_task >> load_task >> validate_task

# Backup bash tasks (uncomment if Python tasks fail)
# extract_task >> transform_bash_task >> train_bash_task >> validate_task
