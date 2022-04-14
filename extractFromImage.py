import base64
from pytesseract import pytesseract
from pytesseract import Output
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import argparse
import cv2
from base64 import b64decode
from urllib import request


def imageScaling(image):
        #== Parameters =======================================================================
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0,0.0,1.0) # In BGR format

    #== Processing =======================================================================

    #-- Read image -----------------------------------------------------------------------
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #-- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    #-- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    #_, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Previously, for a previous version of cv2, this line was: 
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Thanks to notes from commenters, I've updated the code but left this note
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = image.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    return masked  
                                     # Display
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-l", "--lang", required=True,
	help="language that Tesseract will use when OCR'ing")
args = vars(ap.parse_args())

path_to_tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
custom_config = r'-c preserve_interword_spaces=1 --oem 3 --psm 3 -l ' + args["lang"] + '+ita'

newText = ''
pytesseract.tesseract_cmd = path_to_tesseract

image = cv2.imread(args["image"])
#image = cv2.bitwise_not(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#data_uri = base64.b64encode(open(args["image"], 'rb').read()).decode('utf-8')
#img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)

#header,encoded = img_tag.split(",", 1)
#print(header)
#data = b64decode(encoded)

# Python 3.4+
#with request.urlopen(data_uri) as response:
#     data = response.read()

#with open("image.png", "wb") as f:
#    f.write(data)

#print(img_tag)

#imageScaled = imageScaling(image)
#di = pytesseract.image_to_data(imageScaled, config=custom_config, output_type=Output.DICT)
#textScaled = pytesseract.image_to_string(imageScaled)
#print(textScaled)

d = pytesseract.image_to_data(gray, config=custom_config, output_type=Output.DICT)
df = pd.DataFrame(d)

df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')]
sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
for block in sorted_blocks:
    curr = df1[df1['block_num']==block]
    sel = curr[curr.text.str.len()>1]
    char_w = (sel.width/sel.text.str.len()).mean()
    prev_par, prev_line, prev_left = 0, 0, 0
    text = ''
    for ix, ln in curr.iterrows():
        #print("this is prev_par : " + str(prev_par))
        #print("this is the ln['par_num'] : " + str(ln['par_num']))
        if prev_par != ln['par_num']:
            text += '\n'
            prev_par = ln['par_num']
            prev_line = ln['line_num']
            prev_left = 0
        elif prev_line != ln['line_num']:
            #print("this is the ln['line_num'] : " + str(ln['line_num']))
            text += '\n'
            prev_line = ln['line_num']
            prev_left = 0

        added = 0 
        if ln['left']/char_w > prev_left + 1:
            added = int((ln['left'])/char_w) - prev_left
            text += ' ' * added 
        text += ln['text'] + ' '
        prev_left += len(ln['text']) + added + 1
    text += '\n'
    print(text)
