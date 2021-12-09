# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user = scrapy.Field()
    follower_name = scrapy.Field()
    follower_full_name = scrapy.Field()
    follower_profile_pic_url = scrapy.Field()
    _id = scrapy.Field()
