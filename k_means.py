# Preparing the data from Sheet2 for machine learning
# %pip install openpyxl
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the data from Sheet2
sheet2_data = pd.read_excel('data.xlsx')

# Dropping the 'Unnamed: 0' column if it exists
sheet2_data = sheet2_data.drop(columns=['Unnamed: 0'], errors='ignore')

# Separating features and target variable
X = sheet2_data.drop(columns=['type'])
y = sheet2_data['type']

# Displaying the unique values in the target variable and the first few rows of the features
unique_types = y.unique()
X_head = X.head()

print("Unique values in 'type':", unique_types)
print(X_head)


# Encoding categorical features
label_encoders = {}
for column in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    label_encoders[column] = le

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Displaying the shapes of the resulting datasets
X_train_shape = X_train.shape
X_test_shape = X_test.shape
y_train_shape = y_train.shape
y_test_shape = y_test.shape

X_train_shape, X_test_shape, y_train_shape, y_test_shape

# Setting the random state for reproducibility
random_state = 42

# Applying KMeans clustering with 4 clusters
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=random_state, max_iter=500, n_init=10)
# Fitting the model to the features
X['Cluster'] = kmeans.fit_predict(X)

# Mapping cluster labels to region names
region_mapping = {0: 'forest', 1: 'grassland', 2: 'wetland', 3: 'desert'}
X['Region'] = X['Cluster'].map(region_mapping)

# Creating a KMeans scatter plot with distinct colors for each region
plt.figure(figsize=(10, 6))
sns.scatterplot(data=X, x='lattitude', y='theta', hue='Region', palette=['#FF6347', '#4682B4', '#32CD32', '#FFD700'], s=100)
plt.title('KMeans Clustering by Region based on Latitude and Theta')
plt.xlabel('Latitude')
plt.ylabel('Theta')
plt.legend(title='Region')
plt.grid(True)
plt.show()