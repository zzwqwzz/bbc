# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from scrapyspider.model import WebSiteArticle
from scrapyspider.items import ArticleItem


class TutorialScrapyPipeline:
    def process_item(self, item, spider):
        return item


class PgPipeLine:
    def __init__(self, conn_str):
        self.db = None
        self.session = None
        self.conn_str = conn_str

    @classmethod
    def from_crawler(cls, crawler):
        return cls(conn_str=crawler.settings.get('CONN_STR'))

    def open_spider(self, spider):
        self.db = sqlalchemy.create_engine(self.conn_str)
        Session = sessionmaker(bind=self.db)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()
        self.db.dispose()

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            # request = self.session.query(WebSiteRequest).filter_by(finger=item['finger']).first()
            # if request:
            #     request_id = request.id
            # else:
            #     request_id = 0
            article = WebSiteArticle(site_name = item['site_name'],
                                     title = item['title'],
                                     author = item['author'],
                                     content = item['content'],
                                     publish_time = item['publish_time'])

            self.session.add(article)
            self.session.commit()
            return item
