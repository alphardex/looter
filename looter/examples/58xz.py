import pymongo
import asyncio
import looter as lt
from pprint import pprint

domain = 'http://xz.58.com'
client = pymongo.MongoClient()
db = client.58zf
col = db.xz

async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.cssselect('ul.listUl li')
    for item in items:
        data = dict()
        des = item.cssselect('.des')[0]
        data['title'] = des.cssselect('h2 a')[0].text.strip()
        data['link'] = 'http:' + des.cssselect('h2 a')[0].get('href')
        room = des.cssselect('.room')[0].text.strip()
        room = "".join(room.split())  #remove \xa0
        data['scale'] = room[:6]
        data['area'] = int(room[6:][:-1])
        data['price'] = int(item.cssselect('.listliright .money b')[0].text)
        data['place'] = item.cssselect('.add a')[0].text + item.cssselect('.add a')[-1].text
        data['image'] = 'http:' + item.cssselect('img')[0].get('src')
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/xztongshan/chuzu/pn{n}/?PGTID=0d3090a7-02c5-7dac-62a2-11ee90567837&ClickID=2' for n in range(1, 71)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))