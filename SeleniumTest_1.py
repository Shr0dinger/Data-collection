import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['Leomax']
leodb = db.leodb

### Объявляем для MongoDB ссылки уникальным значением документа  ###
leodb.create_index("link", unique=True)

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get('https://www.leomax.ru/products/tovary_dlya_doma_dachi_i_otdyha/')

p = 0
### Нажимаем кнопку "Показать еще" пока она не пропадет и завершаем цикл по условию. ###
### Установлено ограничение на 2 клика на кнопку ввиду больших времязатрат. ###
while p < 2:
    pos = driver.find_elements(By.CLASS_NAME, 'item-block__wrapper')
    actions = ActionChains(driver)
    actions.move_to_element(pos[-1])
    btn = driver.find_element(By.ID, 'categoryAddMore')
    try:
        btn.click()
        p += 1
    except:
        print("End of page")
        p = 1
    time.sleep(3)

goods = driver.find_elements(By.XPATH, "//div[contains(@class,'col-lg-3 col-md-4 col-sm-6 col-xs-12')]")

links = []
leomax_goods = []

### Создаем список ссылок. ###
for i in goods:
    link = i.find_element(By.XPATH, './/a').get_attribute('href')
    links.append(link)

schet = 0

### Извлекаем данные из драйвера. ###

count = 0
for i in goods:
    leomax = {}

    ### По ссылке из списка 'links' проваливаемся в товарную позицию и получаем бренд и весь текст с описанием. ###
    link = links[schet]
    schet = schet + 1
    driver2 = webdriver.Chrome(options=options)
    driver2.implicitly_wait(10)
    driver2.get(link)
    goods_text = driver2.find_elements(By.XPATH, "//div[contains(@class,'longContent')]")
    for j in goods_text:
        text = j.find_element(By.XPATH, "//div[contains(@class,'longContent')]").text
        try:
            brand = j.find_element(By.XPATH,
                                   "//div[contains(@class,'col-xs-10')]/a[contains(@class,'brand-row__brand-name')]").text
            if brand == '': brand = None
        except:
            brand = None

    ### Возвращаемся на страницу с товарами и получаем остальную информацию. ###

    name = i.find_element(By.CLASS_NAME, "title").text

    ### Иногда у товара отсутствует скидка. Делаем исключение. ###
    try:
        price_new = i.find_element(By.CLASS_NAME, "price-new").text
        ### Извлекаем из новой цены наименование валюты "руб." и присоединяем к "старой" цене, у которой ее нет. ###
        curr = price_new.split()
        try:
            curr = curr[2]
        except:
            curr = curr[1]
        price_old = i.find_element(By.CLASS_NAME, "price-old").text
        price_old = price_old + " " + curr
    except:
        price_new = None
        price_old = i.find_element(By.CLASS_NAME, "price").text

    ### Заполняем словарь ###
    leomax['name'] = name
    leomax['brand'] = brand
    leomax['link'] = link
    leomax['price_new'] = price_new
    leomax['price_old'] = price_old
    leomax['text'] = text.replace('\n', '')
    pprint(leomax)
    leomax_goods.append(leomax)

    ## Записываем список словарей в базу  ###

    try:
        leodb.insert_one(leomax)
        count += 1
    except:
        print('Запись не внесена. Повтор')

## Выводим результат###
for i in leodb.find({}):
    pprint(i)

print(f'Всего записей собрано с сайта: {len(leomax_goods)}')
print(f'Всего записей занесено в базу: {count}')
print(f'Всего записей в базе: {leodb.count_documents({})}')
