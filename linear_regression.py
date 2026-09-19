import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


# Load dataset
df = pd.read_csv("data/house_price.csv")

# Basic dataset information
print("\nDataset shape:")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")

for column in df.columns:
    print(f"- {column}")

# Features
X = df[
    [
        "house_size_m2",
        "rooms",
        "floor",
        "open_kitchen",
        "parking_spaces",
        "house_age",
        "garden",
        "bathrooms",
        "toilets",
        "distance_to_city_center_km",
        "municipality",
        "property_type",
        "sauna",
        "balcony_terrace",
        "heating_system",
        "condition",
        "plot_size_m2",
        "energy_rating"
    ]
]


# Target
y = df["price_thousand_eur"]


# Categorical feature
categorical_features = [
    "municipality",
    "property_type",
    "heating_system",
    "condition",
    "energy_rating"
]


# Numerical features
numerical_features = [
    "house_size_m2",
    "rooms",
    "floor",
    "open_kitchen",
    "parking_spaces",
    "house_age",
    "garden",
    "bathrooms",
    "toilets",
    "distance_to_city_center_km",
    "sauna",
    "balcony_terrace",
    "plot_size_m2"
]


# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "location",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numbers",
            "passthrough",
            numerical_features
        )
    ]
)


# Model pipeline
model = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("regression", LinearRegression())
    ]
)


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Train model
model.fit(X_train, y_train)


# Predictions
predictions = model.predict(X_test)


# Evaluation
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)


print("\nPredictions:")
print(predictions)

# Mean Squared error
print("mse: ", mse)

# R2 Score
print("r2 score: ", r2)

# Mean absolute error
print("mae: ", mae)