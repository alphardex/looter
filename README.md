# looter
To install, just run
``` bash
$ pip install looter
```

## features
- super-light-weight crawler
- automatically generate spider with template
- blazing fast speed with concurrent.futures
- provides shell to debug your crawler

## example
Here's a 3-line image crawler:
First, open it with shell
``` bash
$ looter shell konachan.net/post
```
Then, extract with css and grab images you want!
``` python
>>> links = src.cssselect('a.directlink')
>>> save_imgs(links)
```
And of course, there are more functions for you to discover.

## usage
``` bash
Usage:
  looter genspider <name> <tmpl>
  looter shell [<url>]
  looter (-h | --help | --version)

Options:
  -h --help        Show this screen.
  --version        Show version.
```
Templates available: data, image, dynamic
You can also view [examples](https://github.com/alphardex/looter/tree/master/looter/examples).

## tutorial
以下是中文教程：[猛戳这里](http://nameless.wang/2018/03/07/looter%E2%80%94%E2%80%94%E8%B6%85%E8%BD%BB%E9%87%8F%E7%BA%A7%E7%88%AC%E8%99%AB%E6%A1%86%E6%9E%B6/)