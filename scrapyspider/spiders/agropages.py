import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import ArticleItem
from scrapyspider.de_weight import de_weight
import copy


class Agriculture(Spider):
    name = 'agropages'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

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
            yield scrapy.Request(url=u, callback=self.detail_parse)

    def detail_parse(self, response):
        url = response.url
        title = response.xpath("//section[@class='wrap']//h1/text()").extract()
        title = ' '.join(title)
        try:
            publish_time = response.xpath("//section[@class='wrap']//div[@class='toolbtns tl mt15']/span/text()").extract()[0]
        except:
            publish_time = ''
        try:
            publisher = response.xpath("//section[@class='wrap']//h4/div/a/text()").extract()[0]
        except:
            try:
                publisher = response.xpath("//section[@class='wrap']//div[@id='cont_newstxt']/p[1]/em/strong/text()").extract()[0]
            except:
                publisher = ''
        content = response.xpath("//section[@class='wrap']//div[@id='cont_newstxt']/descendant::text()").extract()
        content = '\n'.join(content)

        item = ArticleItem()
        item['url'] = url
        item['site_name'] = self.name
        item['title'] = title
        item['publish_time'] = publish_time
        item['author'] = publisher
        item['content'] = content
        yield item