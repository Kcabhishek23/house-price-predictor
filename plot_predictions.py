import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression


# 1. LOAD DATASET
df = pd.read_csv("data/house_price.csv")


# 2. DEFINE FEATURES AND TARGET
X = df.drop("price_thousand_eur", axis=1)
y = df["price_thousand_eur"]


# 3. CATEGORICAL FEATURES
categorical_features = [
    "municipality",
    "property_type",
    "heating_system",
    "condition",
    "energy_rating"
]


# 4. PREPROCESS CATEGORICAL DATA
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# 5. SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 6. TRANSFORM DATA
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)


# 7. TRAIN LINEAR REGRESSION
model = LinearRegression()

model.fit(X_train_processed, y_train)

# 8. MAKE PREDICTIONS
predictions = model.predict(X_test_processed)


# 9. PLOT ACTUAL VS PREDICTED
plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    predictions,
    alpha=0.5
)

# Perfect prediction line
min_price = min(y_test.min(), predictions.min())
max_price = max(y_test.max(), predictions.max())

plt.plot(
    [min_price, max_price],
    [min_price, max_price],
    linestyle="--"
)

plt.xlabel("Actual Price (thousand €)")
plt.ylabel("Predicted Price (thousand €)")
plt.title("Linear Regression: Actual vs Predicted Prices")

plt.tight_layout()
plt.show()