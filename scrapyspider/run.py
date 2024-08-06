from scrapy import cmdline

name = 'asiapathways'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())