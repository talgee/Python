# import the necessary packages
from localbinarypatterns import LocalBinaryPatterns
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2

class ImageDesc:
    def __init__(self, prediction=0, image=0):
        self.prediction = prediction
        self.image = image

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--training", required=True,
	help="path to the training images")
ap.add_argument("-e", "--testing", required=True, 
	help="path to the tesitng images")
args = vars(ap.parse_args())

desc = LocalBinaryPatterns(24, 8)
data = []
labels = []
for imagePath in paths.list_images(args["training"]):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)
	labels.append(imagePath)
	data.append(hist)
model = LinearSVC(C=100.0, random_state=42)
model.fit(data, labels)
predictions = []
for imagePath in paths.list_images(args["testing"]):
	print(imagePath)
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)
	prediction = model.predict(hist.reshape(1, -1))
	cv2.putText(image, prediction[0], (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	predictions.append(ImageDesc(prediction,imagePath))
for p in predictions:
	strToCheck = str(p.prediction)
	strToCheck = strToCheck.replace('[','')
	strToCheck = strToCheck.replace(']','')
	strToCheck = strToCheck.replace("'",'')

	imageTest = cv2.imread(strToCheck)
	cv2.imshow("ImageMatched", imageTest)
	cv2.waitKey(0)
	print(strToCheck, p.image)