import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

file_path = 'faithful.csv'
data = pd.read_csv(file_path)

X = data[['eruptions', 'waiting']].values

kmeans = KMeans(n_clusters=5, random_state=0, max_iter=1, n_init=1, init='random')

fig, ax = plt.subplots()
step = 0 

def update_plot():
    global step
    ax.clear()
    
    kmeans.max_iter = step + 1
    kmeans.fit(X)
    
    labels = kmeans.predict(X)
    centroids = kmeans.cluster_centers_
    
    ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
    ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red', label='Centroids')
    ax.set_title(f'K-Means bước {step+1}')
    ax.set_xlabel('Eruptions')
    ax.set_ylabel('Waiting Time')

    plt.draw()

def on_click(event):
    global step
    if event.button == 1:
        step += 1
        update_plot()

fig.canvas.mpl_connect('button_press_event', on_click)

ax.scatter(X[:, 0], X[:, 1], color='blue', label='Dữ liệu ban đầu')
ax.set_title('Nhấp chuột trái để bắt đầu K-Means từng bước')
ax.set_xlabel('Eruptions')
ax.set_ylabel('Waiting Time')


plt.show()
