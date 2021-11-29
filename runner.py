from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LessonSCR1 import settings
from LessonSCR1.spiders.HHsp import HhspSpider
from LessonSCR1.spiders.SJsp import SjspSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhspSpider)
    process.crawl(SjspSpider)
    process.start()
    