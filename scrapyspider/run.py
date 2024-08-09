import os
import time

data = time.strftime('%Y%m%d', time.localtime(time.time()))
print('日期:{}'.format(data))
names = ['agdaily', 'agriculture', 'agropages', 'agupdate', 'asiapathways', 'bbc']
for name in names:
    print('开始爬取{}'.format(name))
    cmd = 'scrapy crawl {} -o D:\\desktop\\scrapyspider\\datas\\{}\\{}_{}.csv'.format(name, name, name, data)
    os.system(cmd)
    print('{}爬取结束'.format(name))
print('爬取结束')