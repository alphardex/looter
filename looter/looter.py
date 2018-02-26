""" Looter, a python package aiming at avoiding unnecessary repetition in
making common crawlers.
Author: alphardex  QQ:2582347430
If any suggestion, please contact me. Thank you for cooperation!

How to realize a image crawler in just four lines:
    >>> import looter as lt
    >>> src = lt.get_source('https://konachan.net/post')
    >>> links = src.cssselect('a.directlink')
    >>> lt.save_imgs(links)

Although it only crawls one page, its function can be easily extended,
that's to say, a whole-site crawler, or even a concurrent one... you name it!

And you can also create a spider using template! (data or image)

Usage:
  looter genspider <name> <tmpl>
  looter (-h | --help | --version)

Options:
  -h --help        Show this screen.
  --version        Show version.
"""
import os
import time
import pymysql
import requests
import functools
import configparser
from lxml import etree
from docopt import docopt
from selenium import webdriver
from urllib.parse import unquote


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
    res = requests.get(url, headers=headers, timeout=timeout)
    res.raise_for_status()
    return res


def get_source(url, **kwargs):
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
    src = etree.HTML(html)
    return src


def retrieve_html(url, **kwargs):
    """
    Save .html file directly to local disk. (Usually for testing purpose)

    params:
        encoding: utf-8
    """
    encoding = kwargs.get('encoding', 'utf-8')
    with open('test.html', 'w', encoding=encoding) as f:
        f.write(send_request(url).text)


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


def run_selenium(url):
    """
    Run selenium driver. (driver is headless-chrome by default)
    """
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(f"user-agent={ua}")
    path = r'D:\Program Files (x86)\chromedriver\chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    print(f"Headless Chrome is connecting to {url}...")
    try:
        driver.set_window_size(1640, 688)
        driver.get(url)
    except TimeoutError as e:
        print("Sorry, but connection timed out.")
        raise e
    print("Successfully connected.")
    return driver


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


def cli():
    argv = docopt(__doc__, version='v1.30')
    template = argv['<tmpl>']
    name = argv['<name>']
    if template not in ['data', 'image']:
        exit('Plz provide a template (data or image)')
    package_path = os.path.dirname(__file__)
    with open(f'{package_path}\\templates\\{template}.tmpl', 'r') as i, open(f'{name}.py', 'w') as o:
        o.write(i.read())


if __name__ == '__main__':
    cli()