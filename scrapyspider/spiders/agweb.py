import scrapy
from newspaper import Article
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem
import copy

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
            art = Article(u)
            art.download()
            art.parse()
            url = art.url
            title = art.title
            publish_time = art.publish_date
            author = ','.join(art.authors)
            text = art.text.split('\n')
            temptext = copy.deepcopy(text)
            for e in temptext:
                if e == '':
                    text.remove('')
            content = '\n'.join(text)
            print(url)
            print(title)
            print(publish_time)
            print(author)
            print(content)

            item = ArticleItem()
            item['url'] = url
            item['site_name'] = self.name
            item['title'] = title
            item['publish_time'] = publish_time
            item['author'] = author
            item['content'] = content
            yield item