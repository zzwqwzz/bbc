import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem

class Asiapathways(Spider):
    name = 'asiapathways'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://www.asiapathways-adbi.org/'
        yield Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        links = response.xpath("//div[@id='main']/div/a/@href").extract()
        for u in links:
            yield scrapy.Request(url=u, callback=self.detail_parse)

    def detail_parse(self, response):
        title = response.xpath("//div[@id='main']/div[1]/h1/text()").extract()
        publish_time = response.xpath("//div[@id='main']/div[1]/div[1]/abbr/text()").extract()
        publisher = response.xpath("//div[@id='main']/div[1]/div[1]/span/span/a/text()").extract()
        paragraph = response.xpath("//div[@id='main']/div[1]/div[2]/p/text()").extract()
        content = '\n'.join(paragraph)

        item = ArticleItem()
        item['site_name'] = self.name
        item['title'] = title
        item['publish_time'] = publish_time
        item['author'] = publisher
        item['content'] = content
        yield item