import requests

from bs4 import BeautifulSoup


URL = "https://ya.ru/?via=ywh1"

# Получение HTML-кода страницы
response = requests.get(URL)
response.raise_for_status()  # Проверка на ошибки запроса

# Парсинг с помощью BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')

# Поиск элемента по классу
weather_link = soup.find('a', class_='home-link2 informers3_item informer3_weather home-link2_color_inherit home-link2_hover_tertiary')


print(weather_link)