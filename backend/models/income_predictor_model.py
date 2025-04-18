import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

# Load or generate data
tiers = {
    "tier_1": {"mean": 30000, "std": 3500, "cities": ["Mumbai", "Bangalore", "Delhi"]},
    "tier_2": {"mean": 25000, "std": 2500, "cities": ["Pune", "Chennai", "Hyderabad"]},
    "tier_3": {"mean": 20000, "std": 4500, "cities": ["Indore", "Nagpur", "Patna"]}
}
job_types = ["ride_hailing", "food_delivery", "grocery_delivery", "gig_marketplace"]

# Create synthetic user profile data
users = []
for i in range(1, 31):
    tier = np.random.choice(list(tiers.keys()))
    city = np.random.choice(tiers[tier]["cities"])
    job_type = np.random.choice(job_types)
    username = f"user{i}"
    password = f"pass{i}"
    users.append([username, password, job_type, city, tier])
user_profiles = pd.DataFrame(users, columns=["username", "password", "job_type", "city", "tier"])

# Create income history for each user
income_data = []
for user in user_profiles.itertuples():
    stats = tiers[user.tier]
    monthly_incomes = np.random.normal(stats["mean"], stats["std"], 3).astype(int)
    income_data.append([user.username] + monthly_incomes.tolist())
income_df = pd.DataFrame(income_data, columns=["username", "month_1", "month_2", "month_3"])

# Merge and prepare training data
merged_df = pd.merge(user_profiles, income_df, on="username")
X = merged_df[["job_type", "tier", "month_1", "month_2", "month_3"]]
y = merged_df["month_3"] + np.random.normal(0, 1000, size=len(merged_df))  # Predicting next month

# Pipeline
categorical_features = ["job_type", "tier"]
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
], remainder="passthrough")

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Save model and data
joblib.dump(pipeline, r"C:\Users\ZS\Documents\Wequity\wequity-fin-wellness\backend\models\income_predictor_model.joblib")
user_profiles.to_csv(r"C:\Users\ZS\Documents\Wequity\wequity-fin-wellness\backend\data\user_profiles.csv", index=False)
income_df.to_csv(r"C:\Users\ZS\Documents\Wequity\wequity-fin-wellness\backend\data\income_history.csv", index=False)