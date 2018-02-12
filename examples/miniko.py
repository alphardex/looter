"""
A simplest one page crawler -- Miniko desu!
"""
from crawltools import get_source, save_img
src = get_source('https://konachan.net/post')
links = src.xpath('//a[@class="directlink largeimg"]/@href')
r = [save_img(link) for link in links]