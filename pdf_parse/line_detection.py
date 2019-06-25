import scipy
from scipy import ndimage
from skimage.measure import regionprops
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
from processing import *
from PIL import Image
from pdf2image import convert_from_path

def convert_pdf_to_jpg(path):
    img_from_path = convert_from_path(path)
    for page in img_from_path:
        page.save(path.split('/')[-1].split('.')[0] + '.jpg', 'JPEG')

def get_img_data(path):
    with Image.open(path) as image:
        im_arr = np.frombuffer(image.tobytes(), dtype=np.uint8)
        im_arr = im_arr.reshape((image.size[1], image.size[0], 3)) 
    print(type(im_arr))
    print(im_arr.shape)
    return im_arr

def get_largest_component_img(img, blur_radius = 0.1, threshold = 50):
	img = np.clip(img-170, a_min = 0, a_max = 255)
	imgf = ndimage.gaussian_filter(img, blur_radius)

	labeled, nr_objects = ndimage.label(imgf > threshold)

	components = regionprops(labeled)
	largest_area = 0
	for component in components:
		if(component.bbox_area > largest_area):
			largest_area = component.bbox_area
			largest_component = component

	return largest_component.image

def getContrastImages(data,labels, forPrinting = False): 
	lis = []
	for idx, img in enumerate(data):
		#printI(img, labels[idx],title = 'Original')
		if forPrinting:
			lis.append(img) #add original image to list for printing so we can show side by side pairs in printImgs

		img = np.clip(img-170, a_min = 0, a_max = 255)
		#printI(img, labels[idx], title = 'Contrast')
		lis.append(np.reshape(img,(1,64,64,1)))
	#printImgs(lis, labels,print_pairs=True)
	return np.concatenate(lis,axis=0)

def printImgs(dataSubset, y, print_pairs = False): 
	fig = plt.figure(figsize=(12,12)) #size of each image
	ax = []
	orig_img = True
	y_idx = 0
	for idx, img in enumerate(dataSubset): 

		if (len(img.shape) ==3):    #need to remove the empty channel dimension(s) required for keras for pyplot.
			img = np.squeeze(img, axis = 2)  
		if(len(img.shape)==4):
			img = np.squeeze(img)

		if print_pairs:
			if orig_img:
				title = "original, y: "#.format(y[y_idx])
			else:
				title = "changed, y: "#.format(y[y_idx])  
				y_idx += 1   # updated every second loop

			orig_img = not orig_img
			cols = 2
		else:
			title = ''
			cols = 4

		ax.append(fig.add_subplot(4,cols, idx+1, title = title)) # The point of the list: ax is to be able to index/manipulate figures/ axes
		ax[-1].set_xticks([])
		ax[-1].set_yticks([])
		plt.imshow(img, cmap = 'gray') #need gray cmap to see true color of images.

	plt.show(block=True)  # this call enables imshows in terminal

# X = get_data()
# print(X.shape)
# img_li = []

# for x in X[32:48]:
# 	img = get_largest_component_img(x)
# 	img = resize(img, (28, 28), anti_aliasing=True)
# 	img_li.append(img)

# printImgs(img_li, 0)

# convert_pdf_to_jpg('Ma1-101-A_ BUILDING A FLOOR PLAN GROUND FLOOR LEVEL - HVAC Rev.13.pdf')
x = get_img_data('skrrttt.jpg')
yuh = get_largest_component_img(x)
print(type(yuh))
print(yuh.shape)