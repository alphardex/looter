""" Looter, a python package aiming at avoiding unnecessary repetition in
making common crawlers.
Author: alphardex  QQ:2582347430
If any suggestion, please contact me. Thank you for cooperation!

Usage:
  looter genspider <name> <tmpl>
  looter shell [<url>]
  looter (-h | --help | --version)

Options:
  -h --help        Show this screen.
  --version        Show version.
"""
import os
import re
import code
import time
import pymysql
import requests
import functools
import webbrowser
import configparser
from lxml import etree
from docopt import docopt
from urllib.parse import unquote
from requests.exceptions import MissingSchema


VERSION = 'v1.38'
banner = f"""
Available objects:
    url          The url of the site you crawled.
    res          The response of the site.
    tree         The source tree, can be parsed by xpath and cssselect.

Available functions:
    fetch        Get the element tree of an HTML page.
    view         View the page in your browser. (test rendering)
    save_imgs    Download images from links.
    alexa_rank   Get the reach and popularity of a site in alexa.

For more info, plz refer to tutorial:
    [cssselect]: http://www.runoob.com/cssref/css-selectors.html
    [xpath]: http://www.runoob.com/xpath/xpath-syntax.html
"""

try:
    cf = configparser.ConfigParser()
    cf.read("db_config.conf")
    host = cf.get("db", "host")
    port = cf.getint("db", "port")
    user = cf.get("db", "user")
    passwd = cf.get("db", "passwd")
    charset = cf.get("db", "charset")
    dbname = cf.get("db", "dbname")
except Exception as e:
    pass


def perf(f):
    """
    A decorator to measure the performance of a specific function.
    """
    @functools.wraps(f)
    def wr(*args, **kwargs):
        start = time.time()
        r = f(*args, **kwargs)
        end = time.time()
        print(f'Time elapsed: {end - start}')
        return r
    return wr


def send_request(url, **kwargs):
    """
    Send an HTTP request to a url.

    params:
        timeout: 60
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36'}
    timeout = kwargs.get('timeout', 60)
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        res.raise_for_status()
    except MissingSchema as e:
        res = requests.get('http://' + url, headers=headers, timeout=timeout)
    return res


def fetch(url, **kwargs):
    """
    Get the element tree of an HTML page, use cssselect or xpath to parse it.
    You needn't specify the attribute (like 'href') of the target, just tag is OK. 
    Please refer to the tutorial of this module, and selector tutorial below:
        cssselect: http://www.runoob.com/cssref/css-selectors.html
        xpath: http://www.runoob.com/xpath/xpath-syntax.html
 
    params:
        encoding: res.encoding
        type: text
    """
    res = send_request(url)
    encoding = kwargs.get('encoding', res.encoding)
    res.encoding = encoding
    type_ = kwargs.get('type', 'text')
    html = res.text if type_ == 'text' else res.content
    tree = etree.HTML(html)
    return tree


def view(url, **kwargs):
    """
    View the page whether rendered properly. (Usually for testing purpose)
    params:
        encoding: utf-8
        name: test
    """
    encoding = kwargs.get('encoding', 'utf-8')
    name = kwargs.get('name', 'test')
    with open(f'{name}.html', 'w', encoding=encoding) as f:
        f.write(send_request(url).text)
    webbrowser.open(f'{name}.html', new=1)


def rectify(name):
    """
    Get rid of illegal symbols of a file name.
    """
    if any(symbol in name for symbol in ['?', '<', '>', '|', '*', '"', ":"]):
        name = ''.join([c for c in name if c not in ['?', '<', '>', '|', '*', '"', ":"]])
    return unquote(name)


@perf
def save_img(url, **kwargs):
    """
    Download image and save it to local disk.

    params:
        max_length: 66
    """
    if hasattr(url, 'tag') and url.tag == 'a':
        url = url.get('href')
    elif hasattr(url, 'tag') and url.tag == 'img':
        url = url.get('src')
    name = rectify(url.split('/')[-1])
    ext = name.split('.')[-1]
    max_length = kwargs.get('max_length', 160)
    name = f"{name[:max_length]}.{ext}"
    name = name[:-4] if name.endswith(f'.{ext}.{ext}') else name
    with open(name, 'wb') as f:
        url = url if url.startswith('http') else f'http:{url}'
        f.write(requests.get(url, stream=True).content)
        print(f'Saved {name}')


def save_imgs(urls):
    """
    Download images from links.
    """
    return [save_img(url) for url in urls]


def link_mysql(fun):
    """
    A decorator to connect to MySQL, it will return a cursor.
    But first you need to create a file named 'db_config.conf',
    and this file should be like this:
    [db]
    host = 127.0.0.1
    port = 3306
    user = root
    passwd = ...
    dbname = ...
    charset = ...
    """
    def wr(*args, **kwargs):
        with pymysql.connect(host=host, port=3306, user=user, passwd=passwd, db=dbname, charset=charset) as cur:
            fun(cur, *args, **kwargs)
    return wr


def alexa_rank(url):
    """
    Get the reach and popularity of a site in alexa.
    It will return a tuple:
    (url, reach_rank, popularity_rank)
    """
    alexa = f'http://data.alexa.com/data?cli=10&dat=snbamz&url={url}'
    page = send_request(alexa).text
    reach_rank = re.findall('REACH[^\d]*(\d+)', page)
    popularity_rank = re.findall('POPULARITY[^\d]*(\d+)', page)
    if reach_rank and popularity_rank:
        print(f'[{url}] REACH: {reach_rank[0]} POPULARITY: {popularity_rank[0]}')
        return url, reach_rank[0], popularity_rank[0]
    else:
        print(f'[{url}] Get rank failed.')
        return


def cli():
    """
    Commandline for looter!
    """
    argv = docopt(__doc__, version=VERSION)

    if argv['genspider']:
        template = argv['<tmpl>']
        name = argv['<name>']
        if template not in ['data', 'image', 'dynamic']:
            exit('Plz provide a template (data, image or dynamic)')
        package_path = os.path.dirname(__file__)
        with open(f'{package_path}\\templates\\{template}.tmpl', 'r') as i, open(f'{name}.py', 'w') as o:
            o.write(i.read())

    if argv['shell']:
        if not argv['<url>']:
            url = input('Which site do u want to crawl?\nurl: ')
        else:
            url = argv['<url>']
        res = send_request(url)
        tree = etree.HTML(res.text)
        allvars = {**locals(), **globals()}
        code.interact(local=allvars, banner=banner)


if __name__ == '__main__':
    cli()