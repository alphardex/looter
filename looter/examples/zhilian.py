import asyncio
import looter as lt
from pprint import pprint

domain = 'http://sou.zhaopin.com'

async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.cssselect('.newlist_list_content table.newlist')[1:]
    for item in items:
        data = dict()
        data['name'] = 'python'
        data['link'] = item.cssselect('a')[0].get('href')
        data['company'] = item.cssselect('a')[1].text
        salary = item.cssselect('td.zwyx')[0].text
        if salary in ['面议', '1000元以下']:
            data['salary_min'] = data['salary_max'] = salary
        else:
            data['salary_min'] = int(salary.split('-')[0])
            data['salary_max'] = int(salary.split('-')[1])
        data['place'] = item.cssselect('td.gzdd')[0].text
        pprint(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/jobs/searchresult.ashx?jl=上海%2b苏州&kw=python&isadv=0&sg=bbbda5d40428428dae7931c631a62520&p={i}' for i in range(1, 73)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))