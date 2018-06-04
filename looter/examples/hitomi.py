import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://hitomi.la'
client = pymongo.MongoClient()
db = client.hitomi
col = db.gamecg

def crawl(url):
    tree = lt.fetch(url)
    posts = tree.cssselect('.cg')
    for post in posts:
        data = dict()
        title = post.cssselect('h1 a')[0]
        name = title.text
        data[name] = dict()
        detail = data[name]
        detail['url'] = domain + title.get('href')
        detail['artist'] = post.cssselect('.artist-list')[0].text
        dj_content = post.cssselect('.dj-content .dj-desc')[0]
        td = dj_content.cssselect('tr td')
        detail['series'] = td[1].text.strip() or 'N/A'
        detail['type'] = td[3].cssselect('a')[0].text.strip()
        detail['language'] = td[5].text.strip()
        detail['tags'] = ', '.join([tag.text for tag in td[7].cssselect('.relatedtags ul li a')]) or 'N/A'
        detail['date'] = post.cssselect('.dj-content p.cg-date')[0].text
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/type/gamecg-all-{i}.html' for i in range(1, 2000)]
    with futures.ThreadPoolExecutor(30) as executor:
        executor.map(crawl, tasklist)