import matplotlib.pyplot as plt
import pandas as pd

# LOAD DATA
df = pd.read_csv("data/house_price.csv")


# DATASET GRAPH
plt.figure(figsize=(8, 6))

plt.scatter(
    df["house_size_m2"],
    df["price_thousand_eur"],
    alpha=0.5
)

plt.xlabel("House Size (m²)")
plt.ylabel("Price (thousand €)")
plt.title("House Size vs House Price")

plt.tight_layout()
plt.show()