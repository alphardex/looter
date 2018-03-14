import asyncio
import looter as lt
from pprint import pprint

domain = 'https://nyaa.si'

async def crawl(url):
    tree = await lt.async_fetch(url)
    posts = tree.cssselect('tr.default')
    for post in posts:
        data = dict()
        data['name'] = post.cssselect('td[colspan="2"] a')[-1].get('title')
        data['category'] = post.cssselect('td[style="padding:0 4px;"] a')[-1].get('title')
        link_and_magnet = post.cssselect('td.text-center')[0]
        data['link'] = domain + link_and_magnet.cssselect('a')[0].get('href')
        data['magnet'] = link_and_magnet.cssselect('a')[1].get('href')
        data['size'] = post.cssselect('td.text-center')[1].text
        data['date'] = post.cssselect('td.text-center')[2].text
        data['seeders'] = int(post.cssselect('td.text-center')[3].text)
        data['leechers'] = int(post.cssselect('td.text-center')[4].text)
        data['downloads'] = int(post.cssselect('td.text-center')[5].text)
        pprint(data)
        # You can define your save_data function in advance and call it here :)


if __name__ == '__main__':
    tasklist = [f'{domain}/?p={i}' for i in range(1, 900)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))