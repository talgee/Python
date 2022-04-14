import sys
import os
from colordescriptor import ColorDescriptor
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from rootsift import RootSIFT
from searcher import Searcher
import glob

def mse(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def compare_images(imageA, imageB, title):
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	ax = fig.add_subplot(1, 2, 1)
	#plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
	ax = fig.add_subplot(1, 2, 2)
	#plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
	#plt.show()

	return m,s

def compareByRootSift(image, imageToCompare, name):
	detector = cv2.xfeatures2d.SIFT_create()
	kps = detector.detect(image)
	kpsToCompare = detector.detect(imageToCompare)

	rs = RootSIFT()
	(kps, descs) = rs.compute(image, kps)
	(kpsToCompare, descsToCompare) = rs.compute(imageToCompare, kpsToCompare)

	bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
	matches = bf.match(descs,descsToCompare)

	matches = sorted(matches, key = lambda x:x.distance)

	count = 0
	for m in matches:
		count+=1
	return count

def CompareByColor(image,index):
	cd = ColorDescriptor((8, 12, 3))

	query = cv2.imread(image)
	features = cd.describe(query)
	searcher = Searcher(index)
	results = searcher.search(features)
	return(results[0])


class Result:
    def __init__(self, ssim=0, image=0):
        self.ssim = ssim
        self.image = image

class ImageDesc:
    def __init__(self, name=0, image=0):
        self.name = name
        self.image = image

originalImagePath = r"C:\Users\TalGeva\Downloads\VidasImages\testing\area_rug.png"
original = cv2.imread(r"C:\Users\TalGeva\Downloads\VidasImages\testing\area_rug.png")
index = r"C:\Users\TalGeva\Downloads\Index\index.csv"
dateSetPath = r"C:\Users\TalGeva\Downloads\AllImages"
dataset = glob.glob(r"C:\Users\TalGeva\Downloads\VidasImages\training\area_rug" + "/*.png")

resized_original_image = cv2.resize(original, (100, 50)) 
original = cv2.cvtColor(resized_original_image, cv2.COLOR_BGR2GRAY)

imagesToCheck = []
imageDescs = []
max = 0
indexOfPic = 0
identicalKPS = 0
results = Result(0, 0)

for idx, ds in enumerate(dataset):
	imagesToCheck.append(cv2.imread(ds))
	imageDescs.append(ImageDesc(ds, cv2.imread(ds)))

for idx, img in enumerate(imageDescs):
	resized_toCheck_image = cv2.resize(img.image, (100, 50)) 
	toCheck = cv2.cvtColor(resized_toCheck_image, cv2.COLOR_BGR2GRAY)
	fig = plt.figure("Images")
	images = ("original", original), ("toCheck", toCheck)
	for (j, (nameOfPic, image)) in enumerate(images):
		ax = fig.add_subplot(1, 3, j + 1)
		ax.set_title(nameOfPic)
		#plt.imshow(image, cmap = plt.cm.gray)
		plt.axis("off")

	#plt.show()

	a,b = compare_images(original, toCheck, "Original vs. toCheck")

	count = compareByRootSift(original, toCheck, img.name)

	if(idx == 0):
		max = b
		mostIdentical = img.image
		indexOfPic = j
		nameOfIdenticalPic = img.name
		mostIdenticalImage_KPS = img.image
		identicalKPS = count
		nameOfIdenticalPic_KPS = img.name
	if(max < b):
		max = b
		mostIdentical = img.image
		indexOfPic = j
		nameOfIdenticalPic = img.name
		
	if(identicalKPS < count):
		identicalKPS = count
		mostIdenticalImage_KPS = img.image
		nameOfIdenticalPic_KPS = img.name
		
results = Result(max, mostIdentical)

print("Most identical using SSIM")
print(results.ssim, nameOfIdenticalPic)
print("")
print("Most identical using RootSIFT")
print(identicalKPS, nameOfIdenticalPic_KPS)
print("")

searchByColorResult = CompareByColor(originalImagePath, index)
print("Most identical using searchByColor")
print(searchByColorResult)