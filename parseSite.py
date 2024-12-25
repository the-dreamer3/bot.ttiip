from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin  # Для формирования абсолютных ссылок

def DictionaryNews(url):
    try:
        # Попытка загрузить страницу
        page = urllib.request.urlopen(url)
        parsed_html = BeautifulSoup(page, features="lxml")
        
        # Поиск всех заголовков новостей
        lines = parsed_html.find_all('h3', attrs={'class': 'btl'})
        dictionaryOfNews = []

        # Итерация по заголовкам
        for x in lines:
            # Извлекаем полный текст заголовка
            text = x.get_text(strip=True)
            # Находим ссылку и формируем полный URL
            link_tag = x.find('a', href=True)
            link = urljoin(url, link_tag['href']) if link_tag else None
            dictionaryOfNews.append([text, link])

        return dictionaryOfNews
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# Пример использования
url = "http://www.ttiip.ru/"
news = DictionaryNews(url)

# Вывод всех новостей с полными ссылками
for item in news:
    print(f"Заголовок: {item[0]}, Ссылка: {item[1]}")
