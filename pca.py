import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Simulating the data loading step (since the file path in the code is not accessible)
data = pd.read_excel('data.xlsx', header=0)  # Assuming 'data.xlsx' is the correct file

# Extracting variables and preprocessing
land_types = data['type']  # Assuming 'type' column exists
variables = data.columns[2:8]  # Selecting columns C to H
X = data[variables]

# Standardizing the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Performing PCA
pca = PCA(n_components=6)
X_pca = pca.fit_transform(X_scaled)

# Explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
print("Explained variance ratio:", explained_variance_ratio)

# Plotting the PCA scatter plot
plt.figure(figsize=(15, 10))
for i in range(6):
    plt.subplot(3, 2, i + 1)
    for land_type in land_types.unique():
        subset = X_pca[land_types == land_type]
        plt.scatter(subset[:, i], np.zeros_like(subset[:, i]), label=land_type, alpha=0.6)
    plt.title('PC' + str(i + 1))
    plt.xlabel('PC' + str(i + 1))
    plt.yticks([])
plt.tight_layout()
plt.show()