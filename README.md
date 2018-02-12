# crawltools
With it, you can write a mini-crawler within 10 lines!
Here's a 4-line image crawler:
``` python
>>> from crawltools import get_source, save_img
>>> src = get_source('https://konachan.net/post')
>>> links = src.xpath('//a[@class="directlink largeimg"]/@href')
>>> r = [save_img(link) for link in links]
```
And of course, you can make it grow as bigger as you can.

## Dependencies
lxml==3.8.0
PyMySQL==0.7.11
selenium==3.4.3
requests==2.18.3
