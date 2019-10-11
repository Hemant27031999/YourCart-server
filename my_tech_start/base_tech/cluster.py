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
from .models import Vendors, Cells

def clusterer():

	colnames = ['vendor_lat', 'vendor_long']
	
	X = pd.read_csv('./../../../../../dataset/Vendors-2019-10-09.csv', names=colnames)
	
	print(X.head())
	
	Y = X[['vendor_lat', 'vendor_long']].values
	
	def distance(x, y):
		lat1, long1 = x[0], x[1]
		lat2, long2 = y[0], y[1]
		return geodesic((lat1, long1), (lat2, long2)).meters
	
	eps0 = 200
	min_vendors = 1
	
	est = DBSCAN(eps=eps0, min_samples=min_vendors, metric=distance).fit(Y)
	X['cluster'] = est.labels_.tolist()
	labels = est.labels_
	
	return labels
	
	#colors = pd.tools.plotting._get_standard_colors(len(labels), color_type='random')
	
	#plt.figure(figsize =(9, 9)) 
	#plt.scatter(Y['Lattitude'], Y['Longitude'])
	# Building the legend 
	#plt.legend((r, g, b, k), ('Label 0', 'Label 1', 'Label 2', 'Label -1'))  
	#plt.show() 

def unique(list1): 
  
    unique_list = [] 
    for x in list1: 
        if x not in unique_list: 
            unique_list.append(x)
    return unique_list

a = clusterer()
print(a)

b = unique(a)
b.sort()

n1 = len(a)
n2 = len(b)

vendors = Vendors.objects.all()

for i in range(n1):
	vendors(i).cell_no = a[i]

Cells.objects.all().delete()

objs = []

for i in range(n2):
	ven = Vendors.objects.filter(cell_no = b[i])
	no = count(ven)
	obj = Cells(cell_no=b[i], cell_lat=ven[0].vendor_lat, cell_long=ven[0].vendor_long, no_vendors=no)
	objs.append(obj)

Cells.objects.bulk_create(objs, n2)

