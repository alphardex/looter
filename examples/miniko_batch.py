"""
A simple linear spider, you can crawl whole site slowly with it.
""" 
from crawltools import get_source, save_imgs
def download(url):
    src = get_source(url)
    links = src.xpath('//a[@class="directlink largeimg"]/@href')
    save_imgs(links)

if __name__ == '__main__':
    tasklist = reversed(list(f'https://konachan.net/post?page={9777-i}' for i in range(1, 9777)))
    r = [download(task) for task in tasklist]
