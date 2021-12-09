# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pprint import pprint
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class InstaparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.insta

    def process_item(self, item, spider):
        collection = self.mongo_base[item['user']]
        collection.insert_one(item)
        return item

class InstaparserPicturePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['follower_profile_pic_url']:
            for i in item['follower_profile_pic_url']:
                try:
                    yield scrapy.Request(i)
                except Exception as e:
                    print(e)
        return item

