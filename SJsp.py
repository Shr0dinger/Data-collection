import scrapy
from scrapy.http import HtmlResponse
from LessonSCR1.items import Lessonscr1Item

class SjspSpider(scrapy.Spider):
    name = 'SJsp'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/yurist.html?geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vakansii/yurist.html']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="icMQ_ bs_sM _3ze9n _1M2AW f-test-button-dalshe f-test-link-Dalshe"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//span[@class='_1e6dO _1XzYb _2EZcW']/a/@href").getall()
        for i in links:
            yield response.follow(i, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//span[@class='_2Wp8I _1e6dO _1XzYb _3Jn4o']//text()").getall()
        url = response.url
        yield Lessonscr1Item(name=name, salary=salary, url=url)
