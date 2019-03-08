from concurrent import futures
from pprint import pprint
import looter as lt
import pymongo

domain = 'https://www.dlsite.com'
client = pymongo.MongoClient()
db = client.dlsite
col = db.pro


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('table.n_worklist tr')
    for item in items:
        data = {}
        data['name'] = item.css('.work_name a::text').extract_first()
        data['link'] = item.css('.work_name a::attr(href)').extract_first()
        data['maker'] = item.css('dd.maker_name a::text').extract_first()
        try:
            data['price'] = int(''.join(item.css('span.work_price::text').extract_first().split(',')))
            data['rate'] = int(item.css('.star_rating::text').re_first('\d+'))
            data['review'] = int(item.css('.work_review a::text').re_first('\d+'))
        except Exception as e:
            print(e)
            data['price'] = 0
            data['rate'] = 0
            data['review'] = 0
        if not data['name']:
            continue
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'https://www.dlsite.com/pro/fsr/=/language/jp/order%5B0%5D/trend/per_page/30/page/{n}' for n in range(1, 11252)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
