href = "http://www.ttiip.ru/"
from bs4 import BeautifulSoup
import urllib.request as urllib2

def DictionaryNews():
    page = urllib2.urlopen(href)
    parsed_html = BeautifulSoup(page, features="lxml")
    lines = parsed_html.body.find_all('h3', attrs={'class':'btl'})
    dictionaryOfNews = []
    for x in lines:
        dictionaryOfNews.append([x.text,x.find('a', href = True)['href']])
    
    return dictionaryOfNews