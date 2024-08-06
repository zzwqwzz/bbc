from scrapy import cmdline
import time

#time = time.strftime('%Y%m%d', time.localtime(time.time()))
#names = ['bbc', 'agriculture', 'asiapathways']
#for name in names:
#    cmd = 'scrapy crawl {} -o D:\\desktop\\scrapyspider\\datas\\{}\\{}_{}.csv'.format(name, name, name, time)
#    cmdline.execute(cmd.split())

name = 'agupdate'
cmd = 'acrapy crawl {}'.format(name)
cmdline.execute(cmd.split())