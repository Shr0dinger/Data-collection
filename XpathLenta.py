from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['News']
newsdb = db.newsdb

### Объявляем для MongoDB ссылки уникальным значением документа  ###
newsdb.create_index("link", unique=True)

news_count = 0
news_count_DB = 0
news_skip = 0

### Выбираем рубрику новостей ###

choise = input('Выберите раздел новостей: Футбол - "1"; Инвестиции - "2"; Политика - "3" ')
if choise == '1': url = 'https://lenta.ru/rubrics/sport/football/'
if choise == '2': url = 'https://lenta.ru/rubrics/economics/investments/'
if choise == '3': url = 'https://lenta.ru/rubrics/russia/politic/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.8'}
source = 'https://lenta.ru'
resp = requests.get(url, headers=headers)
dom = html.fromstring(resp.text)

### Начинаем получать данные главной новости раздела ###

news = dom.xpath("//section[contains(@class,'b-feature js-feature b-feature_news')]")
    ### Получаем ссылку, наименование и преобразовываем их ###
head_link = dom.xpath(".//div[contains(@class,'b-feature__header')]/a/@href")
head_link = (source+head_link[0]).replace('//', '/')
head_link = head_link.replace('/', '//',1)
head_name = dom.xpath(".//div[contains(@class,'b-feature__header')]/a/h1/text()")
head_name = head_name[0].replace('\xa0', ' ')
    ### После получения ссылки меняем параметры ###
url = head_link
resp = requests.get(url, headers=headers)
dom = html.fromstring(resp.text)
news = dom.xpath("//div[contains(@class,'b-topic__header')]")
    ### Получаем строку с датой и преобразовываем ее ###
head_date = dom.xpath(".//time[contains(@class,'g-date')]/text()")
head_date = head_date[0]
head_date = head_date.split(',')
head_date = head_date[1]
head_date = head_date[1:]
    ### Формируем список данных ###
news_data = {}
news_data['name'] = head_name
news_data['date'] = head_date
news_data['link'] = head_link
news_data['source'] = source
news_count = news_count + 1
    ### Записываем данные в базу ###
try:
    newsdb.insert_one(news_data)
    news_count_DB = news_count_DB + 1
except:
    news_skip = news_skip + 1

### Закончили получать данные главной новости раздела ###
### Восстанавливаем исходные параметры раздела новостей ###

if choise == '1': url = 'https://lenta.ru/rubrics/sport/football/'
if choise == '2': url = 'https://lenta.ru/rubrics/economics/investments/'
if choise == '3': url = 'https://lenta.ru/rubrics/russia/politic/'
resp = requests.get(url, headers=headers)
dom = html.fromstring(resp.text)
news = dom.xpath("//div[contains(@class,'b-tag-page')]/div[contains(@class,'news-list')]/div[contains(@class,'news')]")

for i in news:
    news_data = {}

### Получаем данные ###

    name = i.xpath(".//h4/a/text()")
    name_fix = name[0].replace('\xa0', ' ')
    link = i.xpath(".//h4/a/@href")
    link_fix = source+link[0]
    date = i.xpath(".//div[contains(@class,'g-date')]/text()")
    date_fix = date[0]

### Формируем список  ###

    news_data['name'] = name_fix
    news_data['date'] = date_fix
    news_data['link'] = link_fix
    news_data['source'] = source
    news_count = news_count + 1

### Записываем список в базу  ###

    try:
        newsdb.insert_one(news_data)
        news_count_DB = news_count_DB + 1
    except:
        news_skip = news_skip + 1

### Выводим результат и статистику ###

for i in newsdb.find({}):
    pprint(i)

print(f'Обработано записей: {news_count}')
print(f'Записано в базу: {news_count_DB}')
print(f'Пропущено записей: {news_skip}')
print(f'Всего записей: {newsdb.count_documents({})}')
