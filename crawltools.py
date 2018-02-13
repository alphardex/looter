""" Crawltools, a python package aiming at avoiding unnecessary repetition in
making common crawlers.
Author: alphardex  QQ:2582347430
If any suggestion, please contact me. Thank you for cooperation!

How to realize a image crawler in just four lines:
    >>> from crawltools import get_source, save_imgs
    >>> src = get_source('https://konachan.net/post')
    >>> links = src.xpath('//a[@class="directlink largeimg"]/@href')
    >>> save_imgs(links)

Although it only crawls one page, its function can be easily extended,
that's to say, a whole-site crawler, or even a concurrent one... you name it!
"""
import time
import pymysql
import requests
import functools
import configparser
from lxml.html import etree
from selenium import webdriver


__all__ = ["send_request", "get_source", "retrieve_html", "link_mysql", "run_selenium", "save_img", "save_imgs"]


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
    @functools.wraps(f)
    def wr(*args, **kwargs):
        start = time.time()
        r = f(*args, **kwargs)
        end = time.time()
        print(f'Time elapsed: {end - start}')
        return r
    return wr


@perf
def send_request(url, **kwargs):
    """
    usage:
        Send request to a page.

    params:
        timeout: 60
    """
    print(f"Sending requests to {url}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36'}
    timeout = kwargs.get('timeout', 60)
    res = requests.get(url, headers=headers, timeout=timeout)
    res.raise_for_status()
    print("Successfully requested.")
    return res


def get_source(url, **kwargs):
    """
    usage:
        Get the element tree of a HTML page. Use xpath to parse it.

    params:
        encoding: res.encoding
        type: content
    """
    res = send_request(url)
    encoding = kwargs.get('encoding', res.encoding)
    res.encoding = encoding
    type_ = kwargs.get('type', 'content')
    html = res.content if type_ == 'content' else res.text
    src = etree.HTML(html)
    return src


def retrieve_html(url, **kwargs):
    """
    usage:
        Save .html file directly to local disk.(Usually for testing purpose)

    params:
        encoding: utf-8
    """
    encoding = kwargs.get('encoding', 'utf-8')
    with open('test.html', 'w', encoding=encoding) as f:
        f.write(send_request(url).text)


def rectify(name):
    if any(symbol in name for symbol in ['?', '<', '>', '|', '*', '"', ":"]):
        name = ''.join([c for c in name if c not in ['?', '<', '>', '|', '*', '"', ":"]])
    else:
        return name


@perf
def save_img(url, **kwargs):
    """
    usage:
        Download image and save it to local disk.

    params:
        max_length: 66
    """
    name = rectify(url.split('/')[-1])
    ext = name.split('.')[-1]
    max_length = kwargs.get('max_length', 66)
    name = f"{name[:max_length]}.{ext}"
    with open(name, 'wb') as f:
        url = url if url.startswith('http') else f'http:{url}'
        f.write(requests.get(url, stream=True).content)
        print(f'Saved {name}')


def save_imgs(urls):
    """
    usage:
        Download images from links.
    """
    return [save_img(url) for url in urls]


def run_selenium(url):
    """usage: driver = run_selenium(url) """
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
    usage:
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
