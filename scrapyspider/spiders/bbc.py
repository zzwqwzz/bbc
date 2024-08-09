import scrapy
from scrapyspider.items import ArticleItem
from scrapyspider.de_weight import de_weight
import copy
import requests
from fake_useragent import UserAgent
import json
import re

class BbcSpider(scrapy.Spider):
    name = 'bbc'

    def __init__(self, *args, **kwargs):
        super(BbcSpider, self).__init__(*args, **kwargs)
        self.page_num=2
        self.tmp_url = "https://web-cdn.api.bbci.co.uk/xd/content-collection/topic-page-be975404-f0e6-440e-b051-3dca827eab92?country=us&page={}&size=9"
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "User-Agent": self.ua.random,
            "Referer": "https://www.example.com",
            'Cookie': 'name=value; name2=value2',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br'
        }

    def start_requests(self):
        url = 'https://www.bbc.com/news/topics/ce1qrvleggxt'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        urls = set()
        for i in range(self.page_num):
            tmp_response = requests.get(self.tmp_url.format(i), headers=self.headers)
            tmp_response.encoding='utf-8'
            tmp_text = json.loads(tmp_response.text)
            tmp_urls = set([data_i["path"] for data_i in tmp_text["data"]])
            urls=urls.union(tmp_urls)
        tempurl = copy.deepcopy(urls)
        temp = set()
        for u in tempurl:
            result = re.match('.{15}', u)
            if result.group() != '/news/articles/':
                urls.remove(u)
            else:
                temp.add("https://www.bbc.com/" + u)
        urls = copy.deepcopy(temp)
        tempurl = copy.deepcopy(urls)
        urls = de_weight(urls, tempurl, self.name)
        for k in urls:
            yield scrapy.Request(url=k, callback=self.detail_parse)

    def detail_parse(self, response):
        url = response.url
        # 标题
        title = response.xpath("//div[@data-component='headline-block']/h1/text()").extract()[0]
        # 正文
        content_res = response.xpath("//div[@data-component='text-block']/p/text()").extract()
        content = '\n'.join(content_res)

        item = ArticleItem()
        item['url'] = url
        item['site_name'] = 'bbc'
        item['title'] = title
        item['content'] = content
        try:
            item['author'] = response.xpath("//div[@data-component='byline-block']/div/div[1]/time/text()")
        except:
            item['author'] = ''
        try:
            item['publish_time'] = response.xpath("//div[@data-component='byline-block']/div/div[1]/time/text()")
        except:
            item['publish_time'] = ''
        yield item
