# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient


class Lessonscr1Pipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2611

    def process_item(self, item, spider):
        if spider.name == 'HHsp':
            final_salary = self.process_salary(item['salary'])
            item['min_salary'] = final_salary[0]
            item['max_salary'] = final_salary[1]
            del item['salary']
        else:
            final_salary = self.process_salary_SJ(item['salary'])
            item['min_salary'] = final_salary[0]
            item['max_salary'] = final_salary[1]
            del item['salary']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        if len(salary) == 1:
            min = None
            max = None
        elif len(salary) == 7:
            min = salary[1].replace('\xa0', ' ')
            max = salary[3].replace('\xa0', ' ')
        elif len(salary) == 5 and salary[0] == 'от':
            min = salary[1].replace('\xa0', ' ')
            max = None
        else:
            max = salary[1].replace('\xa0', ' ')
            min = None

        return min, max

    def process_salary_SJ(self, salary):
        if len(salary) == 1:
            min = None
            max = None
        elif len(salary) == 3 and salary[0] == 'от':
            max = None
            min = salary[2].replace('\xa0', ' ')
            min = min[:-5]
        elif len(salary) == 3 and salary[0] == 'до':
            min = None
            max = salary[2].replace('\xa0', ' ')
            max = max[:-5]
        elif len(salary) == 7:
            max = salary[4].replace('\xa0', ' ')
            min = salary[0].replace('\xa0', ' ')
        else:
            min = None
            max = salary[0].replace('\xa0', ' ')

        return min, max
