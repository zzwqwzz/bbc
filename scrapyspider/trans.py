import time
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import sessionmaker
from scrapyspider.model import WebSiteArticle_cn
from scrapyspider.utils import Translate, Summarize

data = time.strftime('%Y%m%d', time.localtime(time.time()))
engine = create_engine('postgresql://postgres:difyai123456@127.0.0.1:5432/agriculture')
query = "select * from website_article where created_at = '{}'".format(data)
result = pd.read_sql(query, engine)
session = sessionmaker(engine)
session = session()
for i in range(18, len(result)):
    print("======{}======".format(i + 1))
    r = list(result.loc[i])
    article = WebSiteArticle_cn(site_name = r[2], url = r[1], title = Translate(r[3]), author = r[6], content = Translate(r[4]), publish_time = r[5], summarize = Summarize(r[4]))
    session.add(article)
    session.commit()
    time.sleep(5)
    print('end')