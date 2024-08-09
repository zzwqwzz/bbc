import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem
from scrapyspider.de_weight import de_weight
import copy

class Agriculture(Spider):
    name = 'agdaily'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://www.agdaily.com/category/news/'
        yield Request(url, callback=self.parse)

    def parse(self, response):
        urls = set(response.xpath("//div[@id='archive']//article//header/h1/a/@href").extract())
        tempurl = copy.deepcopy(urls)
        urls = de_weight(urls, tempurl, self.name)
        for u in urls:
            yield scrapy.Request(url=u, callback=self.detail_parse)

    def detail_parse(self, response):
        url = response.url
        title = response.xpath("//div[@class='article_container']//div[@class='container']/h1/text()").extract()[0]
        try:
            publish_time = response.xpath("//div[@class='article_container']//div[@class='container']//time/text()").extract()[0]
        except:
            publish_time = ''
        try:
            publisher = response.xpath("//div[@class='article_container']//div[@class='container']//a[@rel='author']/text()").extract()[0]
        except:
            try:
                publisher = response.xpath("//div[@class='article_container']//div[@class='container']//i[@class='post-author']/text()").extract()[0]
            except:
                publisher = ''
        content = response.xpath("//div[@class='clearfix container']/div[1]/div[1]/p/text()").extract()
        content = '\n'.join(content)

        item = ArticleItem()
        item['url'] = url
        item['site_name'] = self.name
        item['title'] = title
        item['publish_time'] = publish_time
        item['author'] = publisher
        item['content'] = content
        yield item