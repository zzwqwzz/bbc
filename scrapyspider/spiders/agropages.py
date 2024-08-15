import time
from newspaper import Article
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem
from scrapyspider.utils import save, de_weight
import copy


class Agriculture(Spider):
    name = 'agropages'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    data = time.strftime('%Y%m%d', time.localtime(time.time()))

    def start_requests(self):
        url = 'https://news.agropages.com/PageView/NewsListWapView.aspx'
        yield Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        urls = set(response.xpath("//h3/a/@href").extract())
        tempurl = set()
        for t in urls:
            tempurl.add('https://news.agropages.com/' + t)
        urls = copy.deepcopy(tempurl)
        urls = de_weight(urls, tempurl, self.name)
        for u in urls:
            yield Request(url=u, callback=self.detail_parse)

    def detail_parse(self, response):
        url = response.url
        art = Article(url)
        art.download()
        art.parse()
        title = art.title
        publish_time = response.xpath("//div[@class='toolbtns tl mt15']/span/text()").extract()[0]
        author = ','.join(response.xpath("//div[@class='topic-company-comtent pl15']//a/text()").extract())
        text = art.text.split('\n')
        temptext = copy.deepcopy(text)
        for e in temptext:
            if e == '':
                text.remove('')
        content = '\n'.join(text)

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