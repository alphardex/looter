import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://stackoverflow.com'
client = pymongo.MongoClient()
db = client.stackoverflow
col = db.python

def crawl(url):
    tree = lt.fetch(url)
    items = tree.cssselect('.question-summary')
    for item in items:
        data = dict()
        data['question'] = item.cssselect('a.question-hyperlink')[0].text
        data['link'] = domain + item.cssselect('a.question-hyperlink')[0].get('href')
        data['votes'] = int(item.cssselect('.vote-count-post strong')[0].text)
        data['answers'] = int(item.cssselect('.status strong')[0].text)
        data['views'] = int(''.join(item.cssselect('.views')[0].get('title')[:-6].split(',')))
        data['timestamp'] = item.cssselect('.relativetime')[0].get('title')
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/questions/tagged/python?page={n}&sort=votes&pagesize=50' for n in range(1, 1001)]
    with futures.ThreadPoolExecutor(40) as executor:
        executor.map(crawl, tasklist)