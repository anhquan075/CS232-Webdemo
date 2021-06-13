import cv2
from sklearn.cluster import KMeans
import numpy as np
 

def compressImage(img_path, k_value=128):
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if img_path.split('.')[-1].lower() != 'bmp':
        cv2.imwrite(img_path.split('.')[0] + '.bmp', image)
    
    print(image.shape)
    rows = image.shape[0]
    cols = image.shape[1]
    
    image = image.reshape(image.shape[0] * image.shape[1], 1)
    kmeans = KMeans(n_clusters = k_value, n_init=10, max_iter=200)
    kmeans.fit(image)
    
    clusters = np.asarray(kmeans.cluster_centers_,dtype=np.uint8) 
    labels = np.asarray(kmeans.labels_,dtype=np.uint8 )  
    labels = labels.reshape(rows, cols)
    
    # np.save(f'static/compressed/np_file/compressed_{k_value}_bitmap.npy', clusters)    
    cv2.imwrite(f'static/compressed/bitmap_file/compressed_{k_value}_bitmap.bmp', labels)

    recovered_image = np.zeros((labels.shape[0], labels.shape[1], 1), dtype=np.uint8)
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            recovered_image[i, j, :] = clusters[labels[i, j],:]

    cv2.imwrite(f'static/compressed/recovered_image/recovered_image_w_{k_value}.bmp', recovered_image)
