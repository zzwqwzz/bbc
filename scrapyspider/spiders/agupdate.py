import scrapy
from scrapy import Request
from newspaper import Article
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem
from scrapyspider.utils import save, de_weight
import copy
import time
import re

class Agupdate(Spider):
    name = 'agupdate'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    data = time.strftime('%Y%m%d', time.localtime(time.time()))

    def start_requests(self):
        url = 'https://agupdate.com/news/'
        yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        urls = set(response.xpath("//a[@class='tnt-asset-link']/@href").extract())
        tempurl = copy.deepcopy(urls)
        temp = set()
        for u in tempurl:
            if re.match("^.*/ads/.*$", u) != None:
                urls.remove(u)
            elif re.match("^.*/places/.*$", u) != None:
                urls.remove(u)
            elif u.startswith("https://agupdate.com"):
                temp.add(u)
            else:
                temp.add("https://agupdate.com/" + u)
        urls = copy.deepcopy(temp)
        tempurl = copy.deepcopy(urls)
        urls = de_weight(urls, tempurl, self.name)
        for u in urls:
            yield Request(url=u, callback=self.detail_parse)

    def detail_parse(self, response):
        url = response.url
        art = Article(url)
        art.download()
        art.parse()
        title = response.xpath("//header[@class='asset-header']/h1/span/text()").extract()[0]
        try:
            publish_time = \
            response.xpath("//header[@class='asset-header']//li[@class='hidden-print']/time[1]/text()").extract()[0]
        except:
            publish_time = ''
        try:
            author = response.xpath("//header[@class='asset-header']/div[2]/span/ul/li[1]/span/a/text()").extract()[0]
        except:
            try:
                author = \
                response.xpath("//header[@class='asset-header']/div[2]/span/ul/li[1]/span/text()").extract()[0]
            except:
                try:
                    author = response.xpath("//header[@class='asset-header']//span[@itemprop='author']/text()").extract()[0]
                except:
                    author = ''
        author = author.split('\n')
        tempauthor = copy.deepcopy(author)
        for e in tempauthor:
            if e == '':
                author.remove('')
        author = ','.join(author)
        content = response.xpath("//div[@id='article-body']/div/p/text()").extract()
        content = '\n'.join(content)

        save(self.name, self.data, art.html, title)

        item = ArticleItem()
        item['url'] = url
        item['site_name'] = self.name
        item['title'] = title
        item['publish_time'] = publish_time
        item['author'] = author
        item['content'] = content
        time.sleep(1)
        yield item