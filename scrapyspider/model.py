from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Index, TIMESTAMP, URL
from datetime import datetime
import time


Base = declarative_base()

class WebSiteArticle(Base):
    __tablename__ = 'website_article'
    __tabl_args__ = '网站信息详情2.0'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), comment='链接')
    site_name = Column(String(255), comment='网站名')
    title = Column(Text, comment='标题')
    content = Column(Text, comment='内容')
    publish_time = Column(String(100), comment='出版时间')
    author = Column(String(255), comment='作者')
    created_at = Column(String(10), nullable=False, default=time.strftime('%Y%m%d', time.localtime(time.time())))
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class WebSiteArticle_cn(Base):
    __tablename__ = 'website_article_cn'
    __tabl_args__ = '网站信息详情2.0'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), comment='链接')
    site_name = Column(String(255), comment='网站名')
    title = Column(Text, comment='标题')
    content = Column(Text, comment='内容')
    publish_time = Column(String(100), comment='出版时间')
    author = Column(String(255), comment='作者')
    summarize = Column(String(1000), comment='摘要')
    created_at = Column(String(10), nullable=False, default=time.strftime('%Y%m%d', time.localtime(time.time())))
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)