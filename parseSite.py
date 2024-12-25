from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin

def DictionaryNews(url):
    try:
        # Установка User-Agent для подмены заголовка запроса
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.1 Safari/537.36'}
        request = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(request)
        parsed_html = BeautifulSoup(page, features="lxml")
        lines = parsed_html.find_all('h3', attrs={'class': 'btl'})
        dictionaryOfNews = []

        for x in lines:
            text = x.get_text(strip=True)
            link_tag = x.find('a', href=True)
            link = urljoin(url, link_tag['href']) if link_tag else None
            dictionaryOfNews.append([text, link])

        return dictionaryOfNews
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

url = "http://www.ttiip.ru/"

