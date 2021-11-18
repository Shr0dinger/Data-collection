# -*- coding: utf-8 -*-
# !/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['VacsHH']
vacsdb = db.vacsdb

vacsdb.create_index("link", unique=True)

vac_list = []
sal_min = ''
sal_max = ''
page = 0
vac_count = 0
vac_skip = 0
vac_count_DB = 0
DB_count = 0

prof = input('Введите название вакансии или ключевое слово: ')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.8'}

params = {'clusters': 'true',
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'search_field': 'name',
          'salary': '',
          'text': prof,
          'page': page}

url = 'https://hh.ru'
resp = requests.get(url + '/search/vacancy', params=params, headers=headers)
dom = BeautifulSoup(resp.text, 'html.parser')

vacs = dom.select('div.vacancy-serp-item')

try:
    pages = dom.find_all('a', {'data-qa': "pager-page"})
    lenpg = len(pages)
    pg_count = int(pages[lenpg - 1].find('span').getText())
except:
    print('Вакасии не найдены!')
    print(f'Обработано страниц: {page}')
    print(f'Обработано записей: {vac_count}')
    print(f'Записано в базу: {vac_count_DB}')
    print(f'Пропущено записей: {vac_skip}')
    for i in vacsdb.find({}):
        DB_count = DB_count + 1
    print(f'Всего записей: {DB_count}')
    raise SystemExit()

while page < pg_count:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.8'}

    params = {'clusters': 'true',
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'search_field': 'name',
              'salary': '',
              'text': prof,
              'page': page}

    url = 'https://hh.ru'
    resp = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(resp.text, 'html.parser')

    vacs = dom.select('div.vacancy-serp-item')

    for i in vacs:
        vac_data = {}
        name = i.find('a', {'class': "bloko-link"}).getText()

        try:
            sal = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText().replace('\u202f', '')
            cur = sal[-4:]
        except:
            sal = None
            cur = None

        try:
            sal = sal[:-5]
            if "от" in sal:
                sal_min = int(sal[3:])
                sal_max = None
            elif "до" in sal:
                sal_max = int(sal[3:])
                sal_min = None
            else:
                sal = sal.split()
                sal_min = int(sal[0])
                sal_max = int(sal[2])
        except:
            sal = None
            sal_min = None
            sal_max = None

        link = i.find('a', {'class': "bloko-link"})['href']

        vac_data['name'] = name
        vac_data['salary_min'] = sal_min
        vac_data['salary_max'] = sal_max
        vac_data['currency'] = cur
        vac_data['link'] = link
        vac_data['site'] = url

        vac_count = vac_count + 1

### Запись полученных данных в базу ###

        try:
            vacsdb.insert_one(vac_data)
            vac_count_DB = vac_count_DB + 1
        except:
            vac_skip = vac_skip + 1

    page = page + 1

for i in vacsdb.find({}):
    DB_count = DB_count + 1

print(f'Обработано страниц: {page}')
print(f'Обработано записей: {vac_count}')
print(f'Записано в базу: {vac_count_DB}')
print(f'Пропущено записей: {vac_skip}')
print(f'Всего записей: {DB_count}')

DB_count = 0

sal_find = int(input('Поиск записей с зарплатой больше, чем: '))

### Поиск зарплаты больше указанной суммы ###

for i in vacsdb.find({'$or': [{'salary_min': {'$gt': sal_find}}, {'salary_max': {'$gt': sal_find}}]}):
    pprint(i)
    DB_count = DB_count + 1

print(f'Записей найдено: {DB_count}')
