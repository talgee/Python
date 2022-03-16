import numpy as np
import cv2

class RootSIFT:
	def __init__(self):
		self.extractor = cv2.xfeatures2d.SIFT_create()

	def compute(self, image, kps, eps=1e-7):
		(kps, descs) = self.extractor.compute(image, kps)
		if len(kps) == 0:
			return ([], None)

		descs /= (descs.sum(axis=1, keepdims=True) + eps)
		descs = np.sqrt(descs)
        
		return (kps, descs)