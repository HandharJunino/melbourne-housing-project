# Melbourne Housing Price Prediction

A machine learning project that predicts Melbourne housing prices using various property features. The project includes data cleaning, exploratory data analysis, model training, and an ETL pipeline orchestrated with Apache Airflow.

## 🏠 Project Overview

This project analyzes Melbourne housing market data to build predictive models for property prices. It includes feature engineering, hyperparameter tuning, and a complete data pipeline for automated processing.

## 📊 Dataset

- **Source**: [Melbourne Housing Snapshot - Kaggle](https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot)
- **Features**: Rooms, Distance, Bathroom, Car spaces, Land size, Postcode, and more
- **Target**: Property prices in AUD

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- PostgreSQL (for data loading)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd melbourne-housing-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

### Running the Project

#### Option 1: Run Individual Scripts

```bash
# Clean and transform data
python scripts/transformation.py

# Train the model
python scripts/train_model.py

# Load data to database
python scripts/load.py
```

#### Option 2: Using Docker

```bash
# Build the image
docker build -t melb-ml .

# Run the pipeline
docker run melb-ml
```

#### Option 3: Using Airflow (Full Pipeline)

```bash
# Start Airflow
docker run -p 8080:8080 -v $(pwd)/dags:/app/dags melb-ml airflow webserver

# Access UI at http://localhost:8080
# Trigger the 'melbourne_housing_etl_pipeline' DAG
```

## 📁 Project Structure

```
melbourne-housing-project/
├── data/
│   ├── raw/                    # Original datasets
│   └── cleaned/                # Processed data
├── models/                     # Trained ML models
├── notebooks/                  # Jupyter notebooks
│   ├── ml_prep.ipynb          # Data preparation
│   ├── ml_model.ipynb         # Model training
│   └── ml_hyperparameters.ipynb  # Hyperparameter tuning
├── scripts/                    # Python scripts
│   ├── transformation.py      # Data cleaning
│   ├── train_model.py         # Model training
│   └── load.py               # Data loading
├── dags/                      # Airflow DAGs
│   └── project_dag.py        # ETL pipeline
├── visualisations/            # Charts and plots
├── requirements.txt           # Python dependencies
├── Dockerfile                # Container configuration
└── README.md                 # This file
```

## 🔧 Scripts Description

### `scripts/transformation.py`
- Cleans raw housing data
- Handles missing values
- Creates feature engineering
- Outputs cleaned dataset

### `scripts/train_model.py`
- Trains Random Forest regression model
- Handles missing price predictions
- Saves trained model as `.pkl` file
- Evaluates model performance

### `scripts/load.py`
- Loads processed data to PostgreSQL
- Supports various database configurations
- Error handling and logging

## 📈 Model Performance

The Random Forest model achieves excellent performance:

### Cross-Validation Results (5-fold):
- **R² Score**: 0.9892 ± 0.0046
- **Mean Absolute Error**: $12,615 ± $4,051
- **RMSE**: $64,348 ± $13,758

### Training Set Performance:
- **R² Score**: 0.9987
- **Mean Absolute Error**: $3,936
- **RMSE**: $23,266

*The model shows strong predictive capability with high R² scores and relatively low prediction errors for Melbourne housing prices.*

## 🔄 ETL Pipeline (Airflow)

The automated pipeline includes:

1. **Extract**: Validate raw data availability
2. **Transform**: Clean and preprocess data
3. **Train**: Build and train ML model
4. **Load**: Save to database
5. **Validate**: Ensure all outputs created

**Schedule**: Daily execution
**Monitoring**: Airflow web UI at `localhost:8080`

## 🛠 Technologies Used

- **Python 3.11**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms
- **Apache Airflow**: Workflow orchestration
- **PostgreSQL**: Data storage
- **Docker**: Containerization
- **Jupyter**: Interactive development

## 📊 Key Features

- **Feature Engineering**: Sale year/month, house age, land size per room
- **Missing Value Imputation**: Smart handling of missing prices
- **Hyperparameter Tuning**: RandomizedSearchCV optimization
- **Cross-Validation**: 5-fold CV for robust evaluation
- **Automated Pipeline**: End-to-end ETL process

## 🔧 Configuration

### Environment Variables (.env)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/housing_db
```

### Docker Configuration
- Base image: `python:3.11-slim`
- Optimized for production deployment
- Non-root user for security

## 📝 Usage Examples

### Training a New Model
```python
from scripts.train_model import train_and_save_model

# Train and save model
model_path = train_and_save_model()
print(f"Model saved to: {model_path}")
```

### Loading Data
```python
from scripts.load import load_to_postgres

load_to_postgres(
    csv_path='data/cleaned/cleaned_data.csv',
    table_name='housing_data',
    db_url='your_database_url'
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Melbourne housing dataset providers
- Scikit-learn community
- Apache Airflow project
- Docker community

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Review the Airflow logs for pipeline errors
3. Ensure all dependencies are installed correctly
4. Verify database connection settings

**Happy house price predicting! 🏡📈**
