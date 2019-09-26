"""
8说了你懂的
"""
import looter as lt

domain = 'https://www.javbus.pw'


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('#waterfall .item')
    for item in items:
        data = {}
        data['name'] = item.css('img::attr(title)').extract_first()
        data['cover'] = item.css('img::attr(src)').extract_first()
        data['link'] = item.css('.movie-box::attr(href)').extract_first()
        data['bango'] = item.css('date::text').extract_first()
        data['date'] = item.css('date::text').extract()[1]
        yield data

if __name__ == '__main__':
    tasklist = [f'{domain}/page/{i}' for i in range(1, 90)]
    total = lt.crawl_all(crawl, tasklist)
    lt.save(total, name='jav.csv', sort_by='date', order='desc')
