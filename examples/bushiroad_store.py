import asyncio
import looter as lt

domain = "https://bushiroad-store.com"
total = []


async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.css(".product-list .product-item")
    for item in items:
        data = {}
        data["link"] = f'{domain}{item.css("a::attr(href)").extract_first()}'
        img_url = (
            item.css("img.product-item__primary-image::attr(data-src)")
            .extract_first()
            .replace("{width}", "800")
        )
        data["img"] = f"https:{img_url}"
        data["name"] = item.css(".product-item__title::text").extract_first()
        price = item.css(".price::text").re_first(r"(\d+,\d{3})|(\d+)").replace(",", "")
        data["price"] = int(price) if price else 0
        data["status"] = item.css("p::text").extract_first().strip()
        total.append(data)


if __name__ == "__main__":
    tasklist = tasklist = [f"{domain}/collections/mygo?page={i}" for i in range(1, 9)]
    loop = asyncio.get_event_loop()
    result = [loop.create_task(crawl(task)) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    lt.save(total, name="bushiroad_store.csv")
