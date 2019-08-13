"""
豆瓣上的“计算机”标签的书籍
"""
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://book.douban.com'
total = []


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('ul.subject-list li.subject-item')
    for item in items:
        data = {}
        data['title'] = item.css('h2 a::text').extract_first().strip()
        data['link'] = item.css('h2 a::attr(href)').extract_first()
        data['pub'] = item.css('.pub::text').extract_first().strip()
        data['rating'] = float(item.css('span.rating_nums::text').extract_first())
        data['comments'] = int(item.css('span.pl').re_first(r'\d+'))
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/tag/%E8%AE%A1%E7%AE%97%E6%9C%BA?start={20 * n}&type=T' for n in range(0, 50)]
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    lt.save(total, name='douban_books.csv', sort_by='comments', order='desc')
