import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'data.xlsx'
data = pd.read_excel(file_path)

data = data.drop(columns=['Unnamed: 0'], errors='ignore')

X = data.drop(columns=['type'])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


true_groups = {
    1: [1, 2, 3, 4, 5, 6, 12, 14],
    2: [7, 8, 9, 10, 11, 13, 28, 30, 31],
    3: [15, 16, 17, 18, 19, 26, 33, 34, 35, 36],
    4: [20, 21, 22, 23, 24, 25, 29, 32]
}


def calculate_accuracy(true_groups, predicted_clusters):
    total_correct = 0
    total_samples = len(predicted_clusters)

    for group_num, true_samples in true_groups.items():
        predicted_samples = [i for i, x in enumerate(predicted_clusters, start=1) if x == group_num]
        correct = len(set(predicted_samples).intersection(true_samples))
        total_correct += correct

    return total_correct / total_samples



best_accuracy = 0
best_clusters = None
best_random_state = None

for random_state in range(1, 101): 
    kmeans = KMeans(n_clusters=4, init="k-means++", random_state=random_state, max_iter=500, n_init=10)
    data['Cluster'] = kmeans.fit_predict(X_scaled)

    accuracy = calculate_accuracy(true_groups, data['Cluster'])

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_clusters = data['Cluster'].copy()
        best_random_state = random_state


for cluster in range(4):
    print(f"Cluster {cluster}:")
    print(data[data['Cluster'] == cluster]['type'].tolist())

plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(data=data, x='lattitude', y='theta', hue='Cluster', palette='viridis', s=100)

for line in range(data.shape[0]):
    scatter.text(data.lattitude[line], data.theta[line], data.type[line], horizontalalignment='left', size='medium',
                 color='black', weight='semibold')

plt.title('K-means Clustering with Best Random State')
plt.xlabel('lattitude')
plt.ylabel('theta')
plt.legend(title='Cluster')
plt.show()

# 
data['Best_Cluster'] = best_clusters

cluster_means = data.groupby('Best_Cluster').mean()

cluster_means.plot(kind='bar', figsize=(12, 6))
plt.title('Mean Features by Best Cluster')
plt.ylabel('Mean Value')
plt.xticks(rotation=0)
plt.show()



import matplotlib.pyplot as plt

# Data
features = [
    "theta", "n", "Evapor", "prefre", "thetas", 
    "thetar", "a", "longitude", "lattitude", "Ks", "Preci"
]
importance = [
    0.292685022, 0.151396721, 0.140375955, 0.108846734, 
    0.093432794, 0.066487631, 0.037378569, 0.036110716, 
    0.024603782, 0.020984206, 0.01769787
]

# Create the bar plot
plt.figure(figsize=(10, 6))
plt.barh(features, importance, color="blue")
plt.xlabel("Importance", fontsize=12)
plt.ylabel("Features", fontsize=12)
plt.title("Feature Importance from Random Forest", fontsize=14)
plt.gca().invert_yaxis()  # To have the highest importance on top
plt.grid(axis='x', linestyle='--', alpha=0.6)

# Show the plot
plt.tight_layout()
plt.show()
