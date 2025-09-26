import asyncio
import looter as lt

domain = 'https://bushiroad-creative.com'
total = []


async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.css(".p-block-c-b.c-grid-responsive-b.c-grid-responsive .p-block-c-b__cell.c-responsive-grid__cell.c-responsive-grid__cell--drop")
    for item in items:
        data = {}
        data["link"] = item.css("a::attr(href)").extract_first()
        data['img'] = item.css("img::attr(src)").extract_first()
        data['label'] = item.css(".p-block-b-a__item__product-icon.c-text.c-text--theme-c-a::text").extract_first()
        data['name'] = item.css(".p-block-c-a__title.c-text::text").extract_first()
        total.append(data)


if __name__ == '__main__':
    tasklist = tasklist = [f'{domain}/products/?lcategory%5B0%5D=1&tg%5B0%5D=46&tg%5B1%5D=47&tg%5B2%5D=48&tg%5B3%5D=49&tg%5B4%5D=50&tg%5B5%5D=51&tg%5B6%5D=52&tg%5B7%5D=53&tg%5B8%5D=54&tg%5B9%5D=55&tg%5B10%5D=56&tg%5B11%5D=57&title=bang-dream&pagenum={i}' for i in range(1, 169)]
    loop = asyncio.get_event_loop()
    result = [loop.create_task(crawl(task)) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    lt.save(total, name='bushiroad_creative.csv')
