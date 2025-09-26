import asyncio
import looter as lt

domain = 'https://bang-dream.com'
total = []


async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.css("ul.itemList li")
    for item in items:
        data = {}
        data["link"] = f'https://bang-dream.com{item.css("a::attr(href)").extract_first()}'
        data['img'] = item.css("img::attr(src)").extract_first()
        data['label'] = item.css(".itemCatLabel::text").extract_first()
        data['name'] = item.css(".itemListText::text").extract_first()
        total.append(data)


if __name__ == '__main__':
    tasklist = tasklist = [f'{domain}/goods?page={i}' for i in range(1, 147)]
    loop = asyncio.get_event_loop()
    result = [loop.create_task(crawl(task)) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    lt.save(total, name='bandori.csv')
