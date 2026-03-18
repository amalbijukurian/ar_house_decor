import numpy as np
from sklearn.cluster import KMeans


def extract_dominant_color(image, mask):

    pixels = image[mask == 255]

    kmeans = KMeans(n_clusters=3)

    kmeans.fit(pixels)

    return kmeans.cluster_centers_[0]