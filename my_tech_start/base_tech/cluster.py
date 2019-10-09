import numpy as np 
import pandas as pd
from sklearn.cluster import DBSCAN 
from geopy.distance import geodesic
from sklearn import metrics
import mpl_toolkits
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler 
from sklearn.preprocessing import normalize 
from sklearn.decomposition import PCA

colnames = ['Lattitude', 'Longitude']

X = pd.read_csv('./../../../../../dataset/melb_data1.csv', names=colnames)

print(X.head())

Y = X[['Lattitude', 'Longitude']].values

def distance(x, y):
	lat1, long1 = x[0], x[1]
	lat2, long2 = y[0], y[1]
	return geodesic((lat1, long1), (lat2, long2)).meters

eps0 = 500
min_vendors = 1

est = DBSCAN(eps=eps0, min_samples=min_vendors, metric=distance).fit(Y)
X['cluster'] = est.labels_.tolist()
labels = est.labels_

print(labels)

#colors = pd.tools.plotting._get_standard_colors(len(labels), color_type='random')

plt.figure(figsize =(9, 9)) 
plt.scatter(Y['Lattitude'], Y['Longitude']) 
  
# Building the legend 
plt.legend((r, g, b, k), ('Label 0', 'Label 1', 'Label 2', 'Label -1')) 
  
plt.show() 