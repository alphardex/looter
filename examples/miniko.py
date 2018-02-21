"""
A simplest one page crawler -- Miniko desu!
"""
import looter as lt
src = lt.get_source('https://konachan.net/post')
links = src.cssselect('a.directlink')
lt.save_imgs(links)
