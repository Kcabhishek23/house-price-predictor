import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


# 1. LOAD DATASET
df = pd.read_csv("data/house_price.csv")



# 2. BASIC DATASET INFORMATION
print("\nDataset shape:")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")

for column in df.columns:
    print(f"- {column}")



# 3. FEATURES
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



# 4. TARGET
y = df["price_thousand_eur"]



# 5. CATEGORICAL FEATURES
categorical_features = [
    "municipality",
    "property_type",
    "heating_system",
    "condition",
    "energy_rating"
]



# 6. NUMERICAL FEATURES
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



# 7. PREPROCESSING
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



# 8. MODEL PIPELINE
model = Pipeline(
    [
        ("preprocessor", preprocessor),
        (
            "regression",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)



# 9. SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 10. TRAIN MODEL
model.fit(X_train, y_train)



# 11. MAKE PREDICTIONS
predictions = model.predict(X_test)



# 12. EVALUATE MODEL
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)


print("\nPredictions:")
print(predictions)


print("\nModel Performance")
print("=" * 40)

print(f"MSE: {mse:.2f}")
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.2f} thousand €")



# 13. PREDICTION FUNCTION
def predict_price(
    house_size,
    rooms,
    floor,
    open_kitchen,
    parking_spaces,
    house_age,
    garden,
    bathrooms,
    toilets,
    distance_to_city_center,
    municipality,
    property_type,
    sauna,
    balcony_terrace,
    heating_system,
    condition,
    plot_size,
    energy_rating
):

    new_house = pd.DataFrame(
        [
            {
                "house_size_m2": house_size,
                "rooms": rooms,
                "floor": floor,
                "open_kitchen": open_kitchen,
                "parking_spaces": parking_spaces,
                "house_age": house_age,
                "garden": garden,
                "bathrooms": bathrooms,
                "toilets": toilets,
                "distance_to_city_center_km": distance_to_city_center,
                "municipality": municipality,
                "property_type": property_type,
                "sauna": sauna,
                "balcony_terrace": balcony_terrace,
                "heating_system": heating_system,
                "condition": condition,
                "plot_size_m2": plot_size,
                "energy_rating": energy_rating
            }
        ]
    )

    prediction = model.predict(new_house)

    return prediction[0]
