import scrapy
from scrapy.http import HtmlResponse
from lerscr.items import LerscrItem
from scrapy.loader import ItemLoader


class PicspSpider(scrapy.Spider):
    name = 'picsp'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{query}/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-name']")
        for i in links:
            yield response.follow(i, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LerscrItem(), response=response)
        loader.add_xpath('name', "//h1//text()")
        loader.add_xpath('price', "//span[@slot='price']//text()")
        loader.add_xpath('pic', "//picture[@slot='pictures']//@src")
        loader.add_value('url', response.url)
        yield loader.load_item()
