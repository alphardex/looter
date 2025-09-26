import asyncio
import looter as lt

domain = "https://bang-dream.com"
total = []


async def crawl(url):
    tree = await lt.async_fetch(url)
    print(url)
    data = {}
    name = tree.css(".pageDetailTitle::text").extract_first()
    if name:
        data["name"] = name.replace("\u3000", " ")
        data["link"] = url
        data["category"] = tree.css(".itemCatLabel::text").extract_first()
        data["imgs"] = tree.css(
            ".pageDetail2columnImage img::attr(src)"
        ).extract_first()
        extraInfosLength = len(tree.css(".itemInfoColumnData::text").extract())
        if extraInfosLength == 5:
            data["sellDate"] = (
                tree.css(".itemInfoColumnData::text").extract_first().strip()
            )
            data["price"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[1]
                .strip()
                .replace(",", "")
            )
            data["size"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[2]
                .strip()
                .replace(",", "")
            )
            data["source"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[3]
                .strip()
                .replace(",", "")
            )
            total.append(data)
        elif (
            extraInfosLength == 4
            and "発売日" in tree.css(".itemInfoArea").extract_first()
            and "サイズ" in tree.css(".itemInfoArea").extract_first()
        ):
            data["sellDate"] = (
                tree.css(".itemInfoColumnData::text").extract_first().strip()
            )
            data["price"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[1]
                .strip()
                .replace(",", "")
            )
            data["size"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[2]
                .strip()
                .replace(",", "")
            )
            data["source"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[3]
                .strip()
                .replace(",", "")
            )
            total.append(data)
        elif (
            extraInfosLength == 4
            and "発売日" in tree.css(".itemInfoArea").extract_first()
        ):
            data["sellDate"] = (
                tree.css(".itemInfoColumnData::text").extract_first().strip()
            )
            data["price"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[1]
                .strip()
                .replace(",", "")
            )
            data["size"] = ""
            data["source"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[2]
                .strip()
                .replace(",", "")
            )
            total.append(data)
        elif (
            extraInfosLength == 4
            and "サイズ" in tree.css(".itemInfoArea").extract_first()
        ):
            data["sellDate"] = ""
            data["price"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[0]
                .strip()
                .replace(",", "")
            )
            data["size"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[1]
                .strip()
                .replace(",", "")
            )
            data["source"] = (
                tree.css(".itemInfoColumnData::text")
                .extract()[2]
                .strip()
                .replace(",", "")
            )
            total.append(data)


if __name__ == "__main__":
    tasklist = tasklist = [f"{domain}/goods/{i}" for i in range(3061, 3872)]
    loop = asyncio.get_event_loop()
    result = [loop.create_task(crawl(task)) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    lt.save(total, name="bandori_detail.csv")
