# FI House Price Predictor

A machine learning project that predicts Finnish style house prices based on property characteristics such as size, rooms, municipality, condition, property type, and other features.

This project was built as part of my journey learning **Machine Learning with Python and Scikit-learn**.

> **Note:** The dataset used in this project is synthetic and was created for machine learning practice. It does not represent actual Finnish housing market transactions.

---

## Project Overview

The goal of this project is to build a regression model that can estimate the price of a property from its characteristics.

The project covers a complete basic machine learning workflow:

* Dataset preparation
* Feature selection
* Categorical data encoding
* Train/test splitting
* Regression modeling
* Model evaluation
* Model comparison
* Prediction
* Streamlit deployment

---

## Machine Learning Model

The final model uses a **Random Forest Regressor** from Scikit-learn.

```python
RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)
```

The model was selected after comparing it with a Linear Regression baseline.

### Model comparison

| Model             |        R² |         MAE |
| ----------------- | --------: | ----------: |
| Linear Regression |     0.854 |     €32.78k |
| Random Forest     | **0.943** | **€19.38k** |

The Random Forest model achieved better performance on this synthetic dataset.

---

## Dataset

The project uses a synthetic Finnish-style dataset containing:

* **10,000 records**
* **18 input features**
* **1 target variable**
* No missing values
* No duplicate records

### Features

#### Property characteristics

* House size
* Rooms
* Floor
* Open kitchen
* Parking spaces
* House age
* Garden
* Bathrooms
* Toilets
* Plot size

#### Location

* Municipality
* Distance to city centre

#### Property details

* Property type
* Sauna
* Balcony / terrace
* Heating system
* Condition
* Energy rating

### Target

```text
price_thousand_eur
```

The target represents the estimated property price in thousands of euros.

---

## Model Performance

The final Random Forest model was evaluated on the test set.

| Metric          |      Result |
| --------------- | ----------: |
| Dataset records |      10,000 |
| R² Score        |  **0.9433** |
| MAE             | **€19.38k** |
| MSE             |  **910.50** |

### What the metrics mean

**R² Score**

Measures how much of the variation in the target values is explained by the model. A value closer to 1 generally indicates better fit on the evaluated dataset.

**MAE — Mean Absolute Error**

Represents the average absolute difference between the predicted and actual prices.

For this model:

```text
MAE ≈ €19,380
```

**MSE — Mean Squared Error**

Measures the average squared difference between predictions and actual values. Larger errors have a stronger effect because the errors are squared.

---

## Application

The project includes a Streamlit web application where users can enter property information and receive a predicted price.

The application allows users to enter:

```text
House size
Rooms
Floor
Open kitchen
Parking spaces
House age
Garden
Bathrooms
Toilets
Distance to city centre
Municipality
Property type
Sauna
Balcony / terrace
Heating system
Condition
Plot size
Energy rating
```

The prediction is generated using the trained Random Forest model.

---

## Project Structure

```text
House Price Predictor/
│
├── data/
│   └── house_price.csv
│
├── main.py
├── app.py
├── README.md
│
├── plot_results.py
├── plot_predictions.py
├── linear_regression.py
```

### Main files

**`main.py`**

Contains the machine learning pipeline, preprocessing, model training, evaluation, and prediction function.

**`app.py`**

Contains the Streamlit user interface and connects the UI to the prediction function from `main.py`.

**`linear_regression.py`**

Used to experiment with and evaluate the linear regression model.

**`plot_results.py`**

Used to visualize the relationship between house size and price.

**`plot_predictions.py`**

Used to visualize actual versus predicted prices.

---

## Machine Learning Workflow

```text
Synthetic Dataset
       ↓
Data Inspection
       ↓
Feature Selection
       ↓
Train / Test Split
       ↓
Categorical Encoding
       ↓
Linear Regression Baseline
       ↓
Random Forest
       ↓
Model Evaluation
       ↓
Prediction
       ↓
Streamlit Application
```

---

## Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Matplotlib

---

## Running the Project

Clone the repository and enter the project directory.

Install the required packages:

```bash
pip install pandas numpy scikit-learn streamlit matplotlib
```

Run the Streamlit application:

```bash
python3 -m streamlit run app.py
```

The application will open in your browser.

---

## Dataset Limitation

This project uses a **synthetic dataset** rather than real Finnish property transaction data.

The dataset was created to provide a realistic environment for learning:

* Regression
* Feature preprocessing
* Categorical encoding
* Model comparison
* Evaluation
* Deployment

Therefore, the model's performance metrics **should not be interpreted as real-world Finnish housing price accuracy**.

---

## What I Learned

Through this project, I practiced:

* Preparing a machine learning dataset
* Selecting useful features
* Separating features and target variables
* Handling categorical variables with `OneHotEncoder`
* Building Scikit-learn pipelines
* Splitting data into training and testing sets
* Understanding regression metrics
* Comparing different ML algorithms
* Using Random Forest for regression
* Building prediction functions
* Connecting an ML model to a Streamlit application
* Presenting an ML project as a portfolio project

---

## Future Improvements

Possible future improvements include:

* Training on real Finnish housing transaction data
* Hyperparameter tuning
* Cross-validation
* Additional model comparisons
* Feature importance analysis
* Better uncertainty estimation
* API deployment with FastAPI
* A separate frontend for the prediction API

---

## Project Purpose

This project was created primarily for **learning and building practical machine learning experience**.

It is not intended to provide professional property valuations or financial advice.

---

**Built with Python, Scikit-learn and Streamlit.**
