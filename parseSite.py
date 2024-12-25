from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin

def DictionaryNews(url):
    try:
        page = urllib.request.urlopen(url)
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
news = DictionaryNews(url)

for item in news:
    print(f"Заголовок: {item[0]}, Ссылка: {item[1]}")
