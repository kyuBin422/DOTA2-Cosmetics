# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   date：          1/2/2021
-------------------------------------------------
   Change Activity:
                   1/2/2021:
-------------------------------------------------
"""
import pickle
import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

matplotlib.style.use('ggplot')

with open('TradeDetail.pickle', 'rb') as handle:
    trend = pickle.load(handle)

sizeL = []
for key in trend:
    sizeL.append(np.size(key, 0))

sizeL = min(sizeL)

for n, key in enumerate(trend):
    trend[n] = key[-sizeL:-1, :]
    trend[n] = trend[n].flatten()

data = np.vstack(trend)

SumSquaredDistances = []
for n_cluster in range(2, 11):
    kmeans = KMeans(n_clusters=n_cluster).fit(data)
    SumSquaredDistances.append(kmeans.inertia_)

plt.plot(range(2, 11), SumSquaredDistances, 'o-')
plt.xlabel("Number of Cluster")
plt.ylabel("Sum Squared Distances")
plt.savefig('image/ElbowPoint.svg', dpi=1200)
