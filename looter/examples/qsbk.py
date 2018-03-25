import asyncio
import looter as lt
from pprint import pprint

domain = 'https://www.qiushibaike.com'
total = []

async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.cssselect('.article')
    for item in items:
        data = dict()
        data['author'] = item.cssselect('h2')[0].text.strip()
        data['content'] = item.cssselect('.content span')[0].text.strip()
        data['vote'] = int(item.cssselect('.stats-vote .number')[0].text)
        data['comments'] = int(item.cssselect('.stats-comments .number')[0].text)
        data['url'] = domain + item.cssselect('a.contentHerf')[0].get('href')
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/hot/page/{i}/' for i in range(1, 14)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    lt.save_as_json(total, name='qsbk', sort_by='vote')