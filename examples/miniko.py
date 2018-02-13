"""
A simplest one page crawler -- Miniko desu!
"""
from crawltools import get_source, save_imgs
src = get_source('https://konachan.net/post')
links = src.xpath('//a[@class="directlink largeimg"]/@href')
save_imgs(links)
