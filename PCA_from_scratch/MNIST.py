import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

# Load the MNIST dataset
print("Loading the MNIST dataset...")
df = pd.read_csv(r'C:\Users\abhis\Downloads\mnist_train.csv')
print("Dataset loaded. Shape:", df.shape)
print("\First few rows:")
print(df.head())

# Filter out labels 1, 0, and 6
print("Filtering data for labels 0, 1, and 6...")
filtered_df = df[df['label'].isin([0, 1, 6])]
print("Filtered data shape:", filtered_df.shape)

# Separate features and labels
X = filtered_df.drop('label', axis=1)
y = filtered_df['label']

# Perform PCA
print("\
Performing PCA...")
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Create scatter plot
print("Creating scatter plot...")
plt.figure(figsize=(10, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', alpha=0.7)
plt.colorbar(scatter)
plt.title('PCA of MNIST data (Labels 0, 1, 6)')
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.legend(handles=scatter.legend_elements()[0], labels=['0', '1', '6'])
plt.show()

print("\
Explained variance ratio:", pca.explained_variance_ratio_)
print("Total explained variance:", sum(pca.explained_variance_ratio_))


from mpl_toolkits.mplot3d import Axes3D

# Perform PCA with 3 components
print("Performing PCA with 3 components...")
pca_3d = PCA(n_components=3)
X_pca_3d = pca_3d.fit_transform(X)

# Create 3D scatter plot
print("Creating 3D scatter plot...")
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
scatter_3d = ax.scatter(X_pca_3d[:, 0], X_pca_3d[:, 1], X_pca_3d[:, 2], c=y, cmap='viridis', alpha=0.7)
ax.set_title('3D PCA of MNIST data (Labels 0, 1, 6)')
ax.set_xlabel('First Principal Component')
ax.set_ylabel('Second Principal Component')
ax.set_zlabel('Third Principal Component')
fig.colorbar(scatter_3d)
plt.show()

print("\
Explained variance ratio (3D):", pca_3d.explained_variance_ratio_)
print("Total explained variance (3D):", sum(pca_3d.explained_variance_ratio_))