import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem

class Agweb(Spider):
    name = 'agweb'
    site = 'https://www.agweb.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://www.agweb.com/news'
        yield Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        links = response.xpath(
            "//div[@class='region region-content']/div[4]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/a/@href").extract()
        link = response.xpath("//div[@class='region region-content']/div[4]/div/div/div[2]/div[1]/div/@about").extract()
        urls = links.union(link)
        for u in urls:
            yield scrapy.Request(url=self.site + u, callback=self.detail_parse)

    def detail_parse(self, response):
        title = response.xpath("//article[@role='article']/h1/text()").extract()
        try:
            publish_time = response.xpath("//article[@role='article']/div[2]/footer/div/div[1]/text()").extract()[2]
        except:
            publish_time = ''
        try:
            publisher = response.xpath("//article[@role='article']/div[2]/footer/div/div[1]/text()").extract()[1]
        except:
            publisher = ''
        content = response.xpath("//article[@role='article']/div[2]/div[2]/p/text()").extract()
        content = '\n'.join(content)

        item = ArticleItem()
        item['site_name'] = self.name
        item['title'] = title
        item['publish_time'] = publish_time
        item['author'] = publisher
        item['content'] = content
        yield item