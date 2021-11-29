import scrapy
from scrapy.http import HtmlResponse
from LessonSCR1.items import Lessonscr1Item

class HhspSpider(scrapy.Spider):
    name = 'HHsp'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82',
        'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&clusters=true&ored_clusters=true&enable_snippets=true&text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for i in links:
            yield response.follow(i, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//div[@class='vacancy-salary']//text()").getall()
        url = response.url
        yield Lessonscr1Item(name=name, salary=salary, url=url)
