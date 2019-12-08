"""
uimovement网站归档
"""
import asyncio
import looter as lt

domain = 'https://uimovement.com'
total = []


async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.css('.resources-wrapper')
    for item in items:
        data = {}
        if item.css('a::text').extract()[0] == 'Sponsor UI Movement':
            continue
        data['title'] = item.css('a::text').extract()[-2]
        data['url'] = f"{domain}{item.css('a::attr(href)').extract_first()}"
        if(vote := item.css('small.vote-count-wrapper::text').extract_first()):
            data['vote'] = int(vote)
        else:
            data['vote'] = 0
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/all-designs/?page={n}' for n in range(1, 501)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    lt.save(total, name='uimovement.csv', no_duplicate=True, sort_by='vote', order='desc')
