from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lerscr.spiders.picsp import PicspSpider
from lerscr import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = 'kraski-dlya-sten-i-potolkov'
    process.crawl(PicspSpider, query=query)
    process.start()
