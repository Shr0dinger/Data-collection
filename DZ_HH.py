# -*- coding: utf-8 -*-
# !/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from pprint import pprint

vac_list = []
sal_min = ''
sal_max = ''
page = 0
prof = input('Введите название вакансии: ')

###Делаем первый запрос и узнаем количетсов страниц###
###Если вакансий нет, и значение = 0 - завершаем программу###

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
    print('Вакасии не найдены')
    raise SystemExit()

###Зная количетсов страниц, делаем условие для цикла###

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
                sal_min = sal[3:]
                sal_max = None
            elif "до" in sal:
                sal_max = sal[3:]
                sal_min = None
            else:
                sal = sal.split()
                sal_min = sal[0]
                sal_max = sal[2]
        except:
            sal = None
            sal_min = None
            sal_max = None

        link = i.find('a', {'class': "bloko-link"})['href']

        vac_data['name'] = name
        vac_data['salary_min'] = sal_min
        vac_data['salary_max'] = sal_max
        vac_data['currency'] = cur

        sep = link.find('?')
        vac_data['link'] = link[:sep]

        vac_data['site'] = url

        vac_list.append(vac_data)

    page = page + 1

### Результат сначала записывается в .csv файл, а затем считывается из него ###

import csv

keys = vac_list[0].keys()
with open('HH.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(vac_list)

import pandas as pd

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

prt = input(f'Количество обработанных страниц: {pg_count}. Хотите вывести результат на экран? (y/n): ')
if prt == 'y':
    DATASET_PATH = './/HH.csv'
    df = pd.read_csv(DATASET_PATH, sep=',')
    print(df)
