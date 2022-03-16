from PIL import Image
import argparse
import cv2
from pytesseract import pytesseract
  
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-l", "--lang", required=True,
	help="language that Tesseract will use when OCR'ing")
args = vars(ap.parse_args())

path_to_tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
  
image = cv2.imread(args["image"])

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  
pytesseract.tesseract_cmd = path_to_tesseract
  
text = pytesseract.image_to_string(threshold_img, lang=args["lang"])

print(text[:-1])