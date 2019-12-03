import numpy as np 
import pandas as pd
from sklearn.cluster import DBSCAN 
from geopy.distance import geodesic
from sklearn import metrics
from math import cos, sin, atan2, sqrt, radians, degrees
import mpl_toolkits
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler 
from sklearn.preprocessing import normalize 
from sklearn.decomposition import PCA
from base_tech.models import Vendors, Cells
import csv
import sqlite3

def clusterer():

	colnames = ['vendor_lat', 'vendor_long']
	
	X = pd.read_csv('out.csv', names=colnames)
	
	print(X.head())

	
	Y = X[['vendor_lat', 'vendor_long']].values

	print(Y[0][0])
	
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
	

def unique(list1): 
  
    unique_list = [] 
    for x in list1: 
        if x not in unique_list: 
            unique_list.append(x)
    return unique_list

def avglatlong(Y):
	print(Y)
	l = len(Y)
	print(l)
	x1 = 0
	y1 = 0
	z1 = 0
	
	for i in range(l):
		print(Y[i][0])
		print(Y[i][1])
		lattitude = radians(90-Y[i][0])
		longitude = radians(Y[i][1])
		x = sin(lattitude)*cos(longitude)
		y = sin(lattitude)*sin(longitude)
		z = cos(lattitude)
		print(x,y,z)
		x1 = x1 + x
		y1 = y1 + y
		z1 = z1 + z

	print(x1,y1,z1)	
	x1 = x1/l
	y1 = y1/l
	z1 = z1/l
	print(x1,y1,z1)
	avg_lat = np.rad2deg(atan2(z1, sqrt((x1*x1)+(y1*y1))))
	avg_long = np.rad2deg(atan2(y1,x1))
	avg = [avg_lat]
	avg.append(avg_long)
	print(avg)
	return avg

def exportcsv():

	conn = sqlite3.connect('./db.sqlite3')
	cursor = conn.cursor()
	cursor.execute("select vendor_lat, vendor_long from base_tech_vendors;")
	with open("out.csv", "w", newline='') as csv_file:  # Python 3 version    
	#with open("out.csv", "wb") as csv_file:              # Python 2 version
	    csv_writer = csv.writer(csv_file)
	  #  csv_writer.writerow([i[0] for i in cursor.description]) # write headers
	    csv_writer.writerows(cursor)

def run():
	exportcsv()
	a = clusterer()
	print(a)
	
	b = unique(a)
	b.sort()
	
	n1 = len(a)
	n2 = len(b)
	
	vendors = Vendors.objects.all()
	
	for i in range(n1):
		Vendors.objects.filter(phone_no=vendors[i].phone_no).update(cell_no=a[i])
	#	vendors[i].update(cell_no = a[i])
	#	vendors[i].save()
	
	Cells.objects.all().delete()
	
	objs = []
	
	for i in range(n2):
		ven = Vendors.objects.filter(cell_no = b[i])
		print(ven)
		no = len(ven)
		list1 = []
		for j in range(no):
			temp = [ven[j].vendor_lat]
			temp.append(ven[j].vendor_long)
			list1.append(temp)
		print(list1)
		avg = avglatlong(list1)
		
		obj = Cells(cell_no=b[i], cell_lat=avg[0], cell_long=avg[1], no_vendor=no)
		objs.append(obj)
	
	Cells.objects.bulk_create(objs, n2)
	
	