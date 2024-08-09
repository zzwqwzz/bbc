import newspaper
from newspaper import Article
import time
times = []
times.append(time.time())
i = 0
cnn_paper = newspaper.build('https://www.agweb.com/', memoize_articles = False)
print(len(cnn_paper.articles))
for article in cnn_paper.articles:
    #if article.url.startswith('https://www.agdaily.com/news') or article.url.startswith('https://www.agdaily.com/lifestyle') or article.url.startswith('https://www.agdaily.com/weather') or article.url.startswith('https://www.agdaily.com/crops') or article.url.startswith('https://www.agdaily.com/livestock') or article.url.startswith('https://www.agdaily.com/technology'):
    print('============================\n')
    print(article.url)
    i += 1
    url = article.url
    art = Article(url)
    art.download()
    art.parse()
    print(art.title)
    print(art.authors)
    print(art.publish_date)
    #print(art.text)
    times.append(time.time())
    print('time{}:{}'.format(i, times[i] - times[i - 1]))
    # else:
    #     continue
print(i)
print('time:{}'.format(times[-1] - times[0]))