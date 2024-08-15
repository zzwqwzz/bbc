import newspaper
from newspaper import Article
import time
times = []
times.append(time.time())
i = 0
# cnn_paper = newspaper.build('https://www.agweb.com/', memoize_articles = False)
# print(len(cnn_paper.articles))
# for article in cnn_paper.articles:
#if article.url.startswith('https://www.agdaily.com/news') or article.url.startswith('https://www.agdaily.com/lifestyle') or article.url.startswith('https://www.agdaily.com/weather') or article.url.startswith('https://www.agdaily.com/crops') or article.url.startswith('https://www.agdaily.com/livestock') or article.url.startswith('https://www.agdaily.com/technology'):
print('============================\n')
#print(article.url)
i += 1
#url = article.url
url = 'https://agupdate.com//iowafarmertoday/news/old-tractors-aren-t-just-for-looks/article_dfa75b42-560c-11ef-b770-f74c29bf5b2c.html'
art = Article(url)
art.download()
art.parse()
with open("D:\\desktop\\scrapyspider\\pages\\test\\test.html", 'w', encoding='utf-8') as f:
    f.write(art.html)
    f.close()
print(art.title)
print(','.join(art.authors))
print(art.publish_date)
t = art.text.split('\n')
for e in t:
    if e == '':
        t.remove('')
t = '\n'.join(t)
print(t)
times.append(time.time())
print('time{}:{}'.format(i, times[i] - times[i - 1]))
# else:
#     continue
print(i)
print('time:{}'.format(times[-1] - times[0]))

from PIL import Image, ImageFont, ImageDraw
import os
import textwrap

# def w2p(text, cutline=True):
# 	# 文字自动换行
# 	if cutline:
# 		sptext = text.split("\n")
# 		hlen = len(sptext)
# 		for i in range(hlen):
# 			sptext[i] = "\n".join(textwrap.wrap(sptext[i],width=35))
# 		text = "\n".join(sptext)
#
# 	# 获取文字列表的最大字符数量
# 	max_len = 0
# 	for item in text.split("\n"):
# 		if len(item) > max_len:
# 			max_len = len(item)
#
# 	# 转换文字为图片并保存为图片
# 	h = 26 * len(text.split("\n")) + 10
# 	w = int(max_len * 19.5 + 10)
# 	im = Image.new("RGB", (w, h), (255, 255, 255))
# 	dr = ImageDraw.Draw(im)
# 	fpath = os.getcwd() + "/msyh.ttf"
# 	font = ImageFont.truetype(fpath, 20)
# 	dr.text((5, 5), text, font=font, fill="#000000")
#
# 	# 存储图片到本地路径/w2p.png
# 	save_path = os.getcwd()
# 	if (os.path.exists(save_path)):
# 		save_path = save_path + "/w2p.png"
# 	else:
# 		os.mkdir(save_path)
# 		save_path = save_path + "/w2p.png"
# 	im.save(save_path)
#
# 	return save_path
#
# text = 'hello world'
# text.parse()