import requests
from bs4 import BeautifulSoup

# URL веб-страницы для парсинга
url = 'https://www.ua-football.com/'

# Отправка GET-запроса к веб-странице
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Использование BeautifulSoup для парсинга HTML-кода страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Создание словаря для хранения данных
    page_data = {}

    # Добавление текстовых данных в словарь
    page_data['text'] = soup.get_text()

    # Добавление заголовков h1 в словарь
    page_data['headings'] = [heading.text for heading in soup.find_all('h1')]

    # Добавление других данных по вашему выбору

    # Вывод словаря
    print(page_data)
else:
    print(f"Ошибка при запросе страницы. Код ответа: {response.status_code}")
