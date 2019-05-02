"""
oreilly上的IT书籍
"""
import looter as lt
from pprint import pprint
from concurrent import futures
import pymongo

domain = 'https://ssearch.oreilly.com'
client = pymongo.MongoClient()
db = client.oreilly
col = db.books


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('#inner_mid_col article')
    for item in items:
        if item.css('p.note::text').extract()[-1][10:] == 'English':
            data = {}
            data['name'] = item.css('p.title a::text').extract_first().strip()
            data['link'] = item.css('p.title a::attr(href)').extract_first().strip()
            data['author'] = item.css('p.note::text').extract_first()[3:]
            data['publisher'] = item.css('p.publisher::text').extract_first()[11:]
            data['year'] = int(''.join(item.css('p.date2::text').extract_first().split())[-4:])
            pprint(data)
            col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/?i=1;m_Sort=relevance;page={n}' for n in range(1, 1196)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
    