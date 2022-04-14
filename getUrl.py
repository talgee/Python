import requests
import re
from lxml.html.clean import clean_html
from bs4 import BeautifulSoup
from html2image import Html2Image

def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    
    for data in soup(['background-color', 'background']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

# open a connection to a URL using urllib
URL = 'https://www.imdb.com/'
  
# Page content from Website URL
page = requests.get(URL)
#print(page.content)
data = remove_tags(page.content)
#print (data)

#print("this is the html : " + str(data))

hti = Html2Image()
html = ""+str(page.content)+""
#print("this is the html : " + html)
css = "body {background: red;}"

hti.screenshot(html_str=html, css_str=css, save_as='white_page.png')