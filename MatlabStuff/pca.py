# Imports
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
#%config InlineBackend.figure_format='retina'

# Load in the data
df = pd.read_csv('CSV_files/SafewayGabor1.csv')

# Standardize the data to have a mean of ~0 and a variance of 1
X_std = StandardScaler().fit_transform(df)

# Create a PCA instance: pca
pca = PCA(n_components=20)
principalComponents = pca.fit_transform(X_std)

# Plot the explained variances
features = range(pca.n_components_)
plt.bar(features, pca.explained_variance_ratio_, color='black')
plt.xlabel('PCA features')
plt.ylabel('variance %')
plt.xticks(features)

plt.show()
# Save components to a DataFrame
PCA_components = pd.DataFrame(principalComponents)

#plt.scatter(PCA_components[0], PCA_components[1], alpha=.1, color='black')
#plt.xlabel('PCA 1')
#plt.ylabel('PCA 2')