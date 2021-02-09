import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from chibabank.items import Article


class ChibaSpider(scrapy.Spider):
    name = 'chiba'
    start_urls = ['https://www.chibabank.co.jp/news/']

    def parse(self, response):
        articles = response.xpath('//div[@class="c-news-03"]')
        for article in articles[1:]:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            link = article.xpath('.//a/@href').get()
            title = article.xpath('.//a/text()').get().strip()
            date = article.xpath('./time/text()').get()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('link', response.urljoin(link))

            yield item.load_item()
