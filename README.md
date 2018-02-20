# looter
To install, just run
``` bash
$ pip install looter
```
With it, you can write a mini-crawler within 10 lines!
Here's a 4-line image crawler:
``` python
>>> import looter as lt
>>> src = lt.get_source('https://konachan.net/post')
>>> links = src.cssselect('a.directlink')
>>> lt.save_imgs(links)
```
And of course, you can make it grow as bigger as you can.
