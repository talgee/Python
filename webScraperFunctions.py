import logging
import queue
import threading
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import os

class webScraperFunctions():
    def DownloadImagesFromHtml(html,i):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('incognito')
        option.add_experimental_option("detach", True)
        driver = webdriver.Chrome('./chromedriver', options=option)
        countNotSuccess = 0
        try:
            path = "Images/"+str(i+1)+"website"
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
            driver.get(html) 
            elemImageList = driver.find_elements_by_tag_name('img')
            for idx, eil in enumerate(elemImageList):
                    src = eil.get_attribute('src')
                    filename, file_extension = os.path.splitext(src)
                    if(file_extension == ""):
                        urllib.request.urlretrieve(src, path+"/"+str(idx+1)+".jpg")
                    else:
                        urllib.request.urlretrieve(src, path+"/"+str(idx+1)+file_extension)
                    #print(src)
            #print("______"+path+"______")
            return path
        except Exception as e: 
            logging.error('error from DownloadImagesFromHtml : ')
            logging.error(e)
            return path


    def scroll(driver,countForScroll):
        SCROLL_PAUSE_TIME = 0.8
        COUNT_FOR_SCROLL = 0
        while COUNT_FOR_SCROLL<countForScroll:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            try:
                driver.find_element_by_class_name('mye4qd').click()
                time.sleep(SCROLL_PAUSE_TIME)
                print("fount btn_____________________________________________________________________________________________")
            except:
                print("")
            COUNT_FOR_SCROLL+=1

    def getHtmlList(imagesToSearch):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('incognito')
        option.add_experimental_option("detach", True)
        #option.add_argument('--disable-dev-sh-usage')
        driver = webdriver.Chrome('./chromedriver', options=option)

        driver.get('https://www.google.com/')
        BeautifulSoup(driver.page_source, 'html.parser')
        driver.find_element_by_name('q').click()
        driver.find_element_by_name('q').send_keys(imagesToSearch + ' photos')
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btnK")))
        driver.find_element_by_name('btnK').click()
        time.sleep(3)

        urlList = []
        urlListToSend = []
        elemList = driver.find_elements_by_xpath("//a[@href]")

        for el in elemList:
            if("https://" in el.text):
                urlList.append(str(el.text.partition("https://")[2]))
        for u in urlList:
            urlListToSend.append(("https://" + u.replace(" › ","/")).replace("leo...",imagesToSearch))
        return urlListToSend

    def getAllImagesFromGoogle(imagesToSearch):
        option = webdriver.ChromeOptions()
        #option.add_argument('--headless')
        option.add_argument('incognito')
        option.add_experimental_option("detach", True)
        #option.add_argument('--disable-dev-sh-usage')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

        driver.get('https://www.google.com/')
        BeautifulSoup(driver.page_source, 'html.parser') 
        driver.find_element_by_name('q').click()
        driver.find_element_by_name('q').send_keys('leonberger photos')
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btnK")))
        driver.find_element_by_name('btnK').click()
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "GmE3X")))
        driver.find_element_by_class_name('GmE3X').click()

        time.sleep(1)
        try:
            path = "Images/Googlewebsite"
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
            webScraperFunctions.scroll(driver,20)
            GoogleElemImageList = driver.find_elements_by_tag_name('img')
            for idx, eil in enumerate(GoogleElemImageList):
                src = eil.get_attribute('src')
                if src is None:
                    continue
                #print(src)
                filename, file_extension = os.path.splitext(src)
                try:
                    if(file_extension == ""):
                        urllib.request.urlretrieve(src, path+"/"+str(idx+1)+".jpg")
                    else:
                        urllib.request.urlretrieve(src, path+"/"+str(idx+1)+file_extension)
                except:
                    continue
            driver.close()
            return path
        except:
            return

