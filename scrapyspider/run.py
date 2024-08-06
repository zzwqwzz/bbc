from scrapy import cmdline

name = 'agweb'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())