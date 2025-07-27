import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('../data/cleaned/cleaned_data.csv')

# prepare the data
df_train = df.dropna(subset=['Price'])
df_missing = df[df['Price'].isna()]

# Feature engineering
features = ['Rooms', 'Distance', 'Bathroom', 'Car', 'Landsize', 'Postcode', 'SaleYear','SaleMonth','HouseAge','LandsizePerRoom','PricePerSqm','RoomsPerBathroom','BuildingDensity'] #

X = df_train[features]
y = df_train['Price']

# train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# predict on the missing values
X_missing = df_missing[features]
predicted_prices = model.predict(X_missing)

# add the predicted prices to the original dataframe
df.loc[df['Price'].isnull(), 'Price'] = predicted_prices
df['Price'] = df['Price'].round(0).astype(int)

# save updated dataframe
df.to_csv('../data/cleaned/cleaned_data_with_predictions.csv', index=False)

target_folder = '../models'

os.makedirs(target_folder, exist_ok=True)
print(f"Ensured directory '{target_folder}' exists.")

# save the model
melb_house_model = os.path.join(target_folder, 'melb_house_model.pkl')

try:
    joblib.dump(model, melb_house_model)
    print(f"Model saved to {melb_house_model}")
except Exception as e:
    print(f"Error loading model: {e}")