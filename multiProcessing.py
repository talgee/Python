import time
import multiprocessing
import argparse

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from webScraperFunctions import webScraperFunctions

if __name__ == '__main__':
    multiprocessing.freeze_support()
    
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageToSearch", required=True,
    help="imageToSearch")
args = vars(ap.parse_args())

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('incognito')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

def dowloadImages(html):
    data = webScraperFunctions.DownloadImagesFromHtml(html)
    print(data)

tic = time.time()
htmlListPath = webScraperFunctions.getHtmlList(args.get("imageToSearch"),driver)
processes = []
#for i in range(len(htmlListPath)):
p = multiprocessing.Process(target=dowloadImages, args=(htmlListPath[0]))
processes.append(p)
p.start()

for process in processes:
    process.join()

toc = time.time()
print('Done in {:.4f} seconds'.format(toc-tic))