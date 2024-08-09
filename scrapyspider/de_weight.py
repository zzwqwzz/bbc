from sqlalchemy import create_engine
import pandas as pd

def de_weight(urls, tempurl, name):
    engine = create_engine('postgresql://postgres:difyai123456@127.0.0.1:5432/test')
    query = "select * from website_article where site_name = '{}'".format(name)
    result = pd.read_sql(query, engine)
    ti = result.loc[-150:, 'url']
    for u in tempurl:
        if len(ti) == 0:
            continue
        else:
            for row in ti:
                if u == row:
                    urls.remove(u)
                    break
                else:
                    continue
    return urls