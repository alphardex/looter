import pymongo
from requestium import Session
from parsel import Selector
from pprint import pprint

domain = 'https://hitomi.la'
client = pymongo.MongoClient()
db = client.hitomi
col = db.gamecg


def crawl(url):
    s.driver.get(url)
    tree = Selector(text=s.driver.page_source)
    gallery_content = tree.css('.gallery-content > div')
    for gallery in gallery_content:
        data = {}
        data['title'] = gallery.css('h1 a::text').extract_first()
        data['link'] = f"{domain}{gallery.css('a::attr(href)').extract_first()}"
        data['artist'] = ', '.join(gallery.css('.artist-list ul li a::text').extract())
        desc = gallery.css('table.dj-desc')
        data['series'] = desc.css('tr:first-child td:nth-child(2)::text').extract_first().strip()
        data['type'] = desc.css('tr:nth-child(2) td:nth-child(2) a::text').extract_first()
        data['tags'] = ', '.join(desc.css('tr:nth-child(4) td:nth-child(2) ul li a::text').extract())
        data['date'] = gallery.css('p.date::text').extract_first()
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    s = Session(webdriver_path='D:\\Program Files (x86)\\chromedriver\\chromedriver.exe', browser='chrome', default_timeout=30, webdriver_options={'arguments': ['headless']})
    tasklist = [f'{domain}/type/gamecg-all-{n}.html' for n in range(1, 100)]
    result = [crawl(task) for task in tasklist]
