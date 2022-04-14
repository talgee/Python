import time
from typing_extensions import Self
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import os
from webScraperFunctions import webScraperFunctions

#def scroll(countForScroll):
#    SCROLL_PAUSE_TIME = 0.8
#    COUNT_FOR_SCROLL = 0
#    while COUNT_FOR_SCROLL<countForScroll:
#        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#        time.sleep(SCROLL_PAUSE_TIME)
#        try:
#            driver.find_element_by_class_name('mye4qd').click()
#            time.sleep(SCROLL_PAUSE_TIME)
#            print("fount btn_____________________________________________________________________________________________")
#        except:
#            print("")
#        COUNT_FOR_SCROLL+=1

option = webdriver.ChromeOptions()
#option.add_argument('--headless')
#option.add_argument('--no-sandbox')incognito
option.add_argument('incognito')
#option.add_experimental_option("detach", True)
#option.add_argument('--disable-dev-sh-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

driver.get('https://www.google.com/')
BeautifulSoup(driver.page_source, 'html.parser')
driver.find_element_by_name('q').click()
driver.find_element_by_name('q').send_keys('Leonberger photos')
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
    urlListToSend.append(("https://" + u.replace(" › ","/")).replace("leo...","Leonberger"))
for uts in urlListToSend:
    print(uts)
time.sleep(3)
countNotSuccess = 0

for idx,ults in enumerate(urlListToSend):
    try:
        path = "Images/"+str(idx+1)+"website"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        driver.get(ults) 
        elemImageList = driver.find_elements_by_tag_name('img')
        for idx, eil in enumerate(elemImageList):
                src = eil.get_attribute('src')
                filename, file_extension = os.path.splitext(src)
                if(file_extension == ""):
                    urllib.request.urlretrieve(src, path+"/"+str(idx+1)+".jpg")
                else:
                    urllib.request.urlretrieve(src, path+"/"+str(idx+1)+file_extension)
                print(src)
        print("______"+path+"______")
    except: 
        continue

    


