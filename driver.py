# import the necessary packages
from rootsift import RootSIFT
import matplotlib.pyplot as plt
import cv2

image = cv2.imread(r"C:\Users\TalGeva\Downloads\car.jpg")
imageToCompare = cv2.imread(r"C:\Users\TalGeva\Downloads\Acura.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayToCompare = cv2.cvtColor(imageToCompare, cv2.COLOR_BGR2GRAY)

detector = cv2.xfeatures2d.SIFT_create()
kps = detector.detect(gray)
kpsToCompare = detector.detect(grayToCompare)

rs = RootSIFT()
(kps, descs) = rs.compute(gray, kps)
(kpsToCompare, descsToCompare) = rs.compute(grayToCompare, kpsToCompare)

print ("RootSIFT: kps="+str(len(kps))+", descriptors="+str(descs.shape))
print ("RootSIFT: kps="+str(len(kpsToCompare))+", descriptors="+str(descsToCompare.shape))

bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
matches = bf.match(descs,descsToCompare)

matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(image, kps, imageToCompare, kpsToCompare, matches[:50], imageToCompare, flags=2)

#print(matches)

cv2.imshow("result", img3)
cv2.waitKey(0)
plt.imshow(img3),
plt.show()