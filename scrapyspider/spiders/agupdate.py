import scrapy
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem
from scrapyspider.de_weight import de_weight
import copy

class Agupdate(Spider):
    name = 'agupdate'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://agupdate.com/news/'
        yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        urls = set(response.xpath("//a[@class='tnt-asset-link']/@href").extract())
        tempurl = copy.deepcopy(urls)
        temp = set()
        for u in tempurl:
            if u.startswith("/midwestmessenger") or u.startswith("/places") or u.startswith("/todaysproducer") or u.startswith("/livestockroundup"):
                urls.remove(u)
            elif u.startswith("https://agupdate.com"):
                temp.add(u)
            else:
                temp.add("https://agupdate.com/" + u)
        urls = copy.deepcopy(temp)
        tempurl = copy.deepcopy(urls)
        urls = de_weight(urls, tempurl, self.name)
        for u in urls:
            if u.startswith("https://agupdate.com"):
                yield scrapy.Request(url=u, callback=self.detail_parse)
            else:
                yield scrapy.Request(url="https://agupdate.com/" + u, callback=self.detail_parse)

    def detail_parse(self, response):
        url = response.url
        title = response.xpath("//header[@class='asset-header']/h1/span/text()").extract()[0]
        try:
            publish_time = response.xpath("//header[@class='asset-header']//li[@class='hidden-print']/time[1]/text()").extract()[0]
        except:
            publish_time = ''
        try:
            publisher = response.xpath("//header[@class='asset-header']//span[@itemprop='author']/text()").extract()[0]
        except:
            try:
                publisher = response.xpath("//header[@class='asset-header']/div[2]/span/ul/li[1]/span/text()").extract()[0]
            except:
                publisher = ''
        content = response.xpath("//div[@id='article-body']/div/p/text()").extract()
        content = '\n'.join(content)

        item = ArticleItem()
        item['url'] = response.url
        item['site_name'] = self.name
        item['title'] = title
        item['publish_time'] = publish_time
        item['author'] = publisher
        item['content'] = content
        yield item