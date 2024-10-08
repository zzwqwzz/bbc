from sqlalchemy.orm import sessionmaker
from scrapyspider.celery import cel
import time
from scrapyspider.model import WebSiteArticle_cn
from scrapyspider.utils import Translate, Summarize
from sqlalchemy import create_engine
import pandas as pd

@cel.task
def auto_trans():
    data = time.strftime('%Y%m%d', time.localtime(time.time()))
    print('日期：{}'.format(data))
    engine = create_engine('postgresql://postgres:difyai123456@127.0.0.1:5432/agriculture')
    query = "select * from website_article where created_at = '{}'".format(data)
    result = pd.read_sql(query, engine)
    session = sessionmaker(engine)
    session = session()
    for i in range(len(result)):
        print('第{}条'.format(i + 1))
        r = list(result.loc[i])
        article = WebSiteArticle_cn(site_name=r[2],
                                 url=r[1],
                                 title=Translate(r[3]),
                                 author=r[6],
                                 content=Translate(r[4]),
                                 publish_time=r[5],
                                 summarize = Summarize(r[4]))
        session.add(article)
        session.commit()
        print('第{}条翻译结束'.format(i + 1))
    print('翻译结束')