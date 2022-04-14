import argparse
from concurrent.futures import thread
import logging
from queue import Queue
from threading import Thread
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from webScraperFunctions import webScraperFunctions
from bs4 import BeautifulSoup
import urllib.request
import os
import concurrent.futures

from yolo5TestsWithYield import checkYOLO_ForPath

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageToSearch", required=True,
    help="imageToSearch")
args = vars(ap.parse_args())

start = time.time()

q = Queue(maxsize=0)
q2 = Queue(maxsize=0)

htmlListPath = webScraperFunctions.getHtmlList(args.get("imageToSearch"))
num_theads = min(50, len(htmlListPath))

results = [{} for x in htmlListPath];
for i in range(len(htmlListPath)):
    q.put(htmlListPath[i])

def crawl(q,i):
    while not q.empty():
        try:
            if (i == 0):
                checkYOLO_ForPath(webScraperFunctions.getAllImagesFromGoogle(args.get("imageToSearch")))
            else:
                checkYOLO_ForPath(webScraperFunctions.DownloadImagesFromHtml(q.get(),i))
        except:
            continue
    return True

#def YOLO(q2):
#    while not q2.empty():
#        try:
#            checkYOLO_ForPath(q2.get())
#        except:
#            continue
#    return True

i = 0
with concurrent.futures.ThreadPoolExecutor() as executor:
    for i in range(num_theads+1):
        print('Starting thread ', i)
        executor.submit(crawl, q,i)
        i = i+1
#with concurrent.futures.ThreadPoolExecutor() as executor1:
#    for i in range(num_theads+1):
#        print('Starting thread for YOLO', i)
#        executor1.submit(YOLO, q2)
#        i = i+1

q.join
#q2.join
print('All tasks completed.')

end = time.time()
print("[INFO] Whole Process took {:.6f} seconds".format(end - start))
