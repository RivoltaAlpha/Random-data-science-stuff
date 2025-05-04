import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Mount Google Drive (if using Colab)
# from google.colab import drive
# drive.mount('/content/drive')

# Define paths for your files
file_paths = [
    '/content/alpha.nc',
    '/content/k_snc.nc',
    '/content/lambda.nc',
    '/content/n.nc',
    '/content/psi.nc',
    '/content/tr.nc',
    '/content/ts.nc'
]

# Define a mapping for variable extraction
variable_map = {
    'alpha': 'VGM_alpha_l1',
    'k_snc': 'k_s_l1',
    'lambda': 'lambda_l1',
    'n': 'VGM_n_l1',
    'psi': 'psi_s_l1',
    'tr': 'VGM_theta_r_l1',
    'ts': 'theta_s_l1'
}

# Generalized function to process data chunks
def process_data_chunks(data, longitude, latitude, variable_name, chunk_size=1000):
    scaler = StandardScaler()
    data = data[::10, ::10]  # Downsample data
    longitude = longitude[::10]
    latitude = latitude[::10]

    # Loop through rows in chunks
    for start_row in range(0, data.shape[0], chunk_size):
        end_row = min(start_row + chunk_size, data.shape[0])
        data_chunk = data[start_row:end_row, :]
        data_scaled = scaler.fit_transform(data_chunk.flatten().reshape(-1, 1))

        # Perform clustering
        n_clusters = 3
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(data_scaled)
        clusters_reshaped = clusters.reshape(data_chunk.shape)

        # Plot the clustered data
        plt.figure(figsize=(10, 6))
        plt.imshow(
            clusters_reshaped,
            cmap='viridis',
            extent=[longitude.min(), longitude.max(), latitude.min(), latitude.max()]
        )
        plt.colorbar(label='Cluster')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Cluster Analysis for {variable_name} (Chunk: {start_row}-{end_row})')
        plt.show()

# Iterate over all files and process variables
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    with h5py.File(file_path, 'r') as hdf_file:
        longitude = hdf_file['longitude'][:]
        latitude = hdf_file['latitude'][:]

        # Determine variable name based on file name
        variable_name = None
        for key in variable_map:
            if key in file_path:
                variable_name = variable_map[key]
                break

        if variable_name and variable_name in hdf_file:
            print(f"Processing variable: {variable_name}")
            data = hdf_file[variable_name][:]
            process_data_chunks(data, longitude, latitude, variable_name)
        else:
            print(f"Variable not found for file: {file_path}")
