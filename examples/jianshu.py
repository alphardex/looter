"""
简书上“程序员”专题下的文章
"""
from pprint import pprint
import looter as lt

domain = 'https://www.jianshu.com'
total = []


def crawl(url):
    try:
        tree = lt.fetch(url)
        items = tree.css('ul.note-list li')
        for item in items:
            data = {}
            data['title'] = item.css('.content a.title::text').extract_first()
            data['author'] = item.css('a.nickname::text').extract_first()
            data['source'] = f"{domain}{item.css('.content a.title::attr(href)').extract_first()}"
            data['vote'] = max(map(int, (item.css('.meta span').re(r'\d+'))))
            pprint(data)
            total.append(data)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    tasklist = [f'{domain}/c/NEt52a?order_by=top&page={n}' for n in range(1, 201)]
    [crawl(task) for task in tasklist]
    lt.save(total, name='jianshu.csv', sort_by='vote', order='desc')
