"""
A simplest one page crawler -- Miniko desu!
"""
from crawltools import *
src = get_source('https://konachan.net/post')
links = src.cssselect('a.directlink')
save_imgs(links)
