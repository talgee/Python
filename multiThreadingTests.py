import requests
from queue import Queue
from threading import Thread
import argparse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webScraperFunctions import webScraperFunctions

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageToSearch", required=True,
    help="imageToSearch")
args = vars(ap.parse_args())

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('incognito')
driver = webdriver.Chrome('./chromedriver', options=option)

NUM_THREADS = 8
q = Queue()

def crawl():
    global q

    while True:
        print(q.get())
        data = webScraperFunctions.DownloadImagesFromHtml(q.get())
        print(data)
        q.task_done()

def download_img():
	"""
	Download image from img_url in curent directory
	"""
	global q

	while True:
		img_url = q.get()
        
		res = requests.get(img_url, stream=True)
		filename = f"{img_url.split('/')[-1]}.jpg"

		with open(filename, 'wb') as f:
			for block in res.iter_content(1024):
				f.write(block)
		q.task_done()


if __name__ == '__main__':
    htmlListPath = webScraperFunctions.getHtmlList(args.get("imageToSearch"),driver)
    
    #for img_url in htmlListPath:
    q.put(htmlListPath[0])

    for t in range(NUM_THREADS):

        worker = Thread(target=crawl)
        worker.daemon = True
        worker.start()

    q.join()