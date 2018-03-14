import os
import re
import time
import asyncio
import aiohttp
import pymysql
import requests
import functools
import webbrowser
import configparser
from lxml import etree
from urllib.parse import unquote


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36'}

if os.path.exists('db_config.conf'):
    cf = configparser.ConfigParser()
    cf.read("db_config.conf")
    host = cf.get("db", "host")
    port = cf.getint("db", "port")
    user = cf.get("db", "user")
    passwd = cf.get("db", "passwd")
    charset = cf.get("db", "charset")
    dbname = cf.get("db", "dbname")


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


def send_request(url:str, **kwargs) -> requests.models.Response:
    """
    Send an HTTP request to a url.

    Args:
        url: The url of the site.
        **kwargs: timeout
    
    Returns:
        The response of the HTTP request.
    """
    timeout = kwargs.get('timeout', 60)
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        res.raise_for_status()
    except requests.exceptions.MissingSchema as e:
        res = requests.get('http://' + url, headers=headers, timeout=timeout)
    return res


def fetch(url:str, **kwargs) -> etree._Element:
    """
    Get the element tree of an HTML page, use cssselect or xpath to parse it.

    Please refer to the tutorial of this module, and selector tutorial below:
        cssselect: http://www.runoob.com/cssref/css-selectors.html
        xpath: http://www.runoob.com/xpath/xpath-syntax.html
 
    Args:
        url: The url of the site.
        **kwargs: encoding, type
    
    Returns:
        The element tree of the HTML page.
    """
    res = send_request(url)
    encoding = kwargs.get('encoding', res.encoding)
    res.encoding = encoding
    type_ = kwargs.get('type', 'text')
    html = res.text if type_ == 'text' else res.content
    tree = etree.HTML(html)
    return tree


def view(url:str, **kwargs):
    """
    View the page whether rendered properly. (Usually for testing purpose)

    Args:
        url: The url of the site.
        **kwargs: encoding, name
    """
    encoding = kwargs.get('encoding', 'utf-8')
    name = kwargs.get('name', 'test')
    with open(f'{name}.html', 'w', encoding=encoding) as f:
        f.write(send_request(url).text)
    webbrowser.open(f'{name}.html', new=1)


def rectify(name:str) -> str:
    """
    Get rid of illegal symbols of a filename.

    Args:
        name: The filename.
    
    Returns:
        The rectified filename.
    """
    if any(symbol in name for symbol in ['?', '<', '>', '|', '*', '"', ":"]):
        name = ''.join([c for c in name if c not in ['?', '<', '>', '|', '*', '"', ":"]])
    return unquote(name)


def get_img_name(url:str, **kwargs) -> str:
    """Get the name of an image.
    
    Args:
        url: The url of the site.
        **kwargs: max_length
    
    Returns:
        The name of an image and its url.
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
    return url, name


@perf
def save_img(url:str):
    """
    Download image and save it to local disk.

    Args:
        url: The url of the site.
    """
    url, name = get_img_name(url)
    with open(name, 'wb') as f:
        url = url if url.startswith('http') else f'http:{url}'
        f.write(requests.get(url ,headers=headers).content)
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


def alexa_rank(url:str) -> tuple:
    """
    Get the reach and popularity of a site in alexa.
    It will return a tuple:
    (url, reach_rank, popularity_rank)

    Args:
        url: The url of the site.
    
    Returns:
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


async def async_fetch(url:str, **kwargs) -> etree._Element:
    """Fetch a webpage in an async style.
    
    Args:
        url: The url of the site.
        **kwargs: type
    
    Returns:
        The element tree of the HTML page.
    """
    type_ = kwargs.get('type', 'text')
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url, headers=headers) as res:
            html = await res.text() if type_ == 'text' else res.read()
            tree = etree.HTML(html)
            return tree


async def async_save_img(url:str, **kwargs):
    """Save an image in an async style.
    
    Args:
        url: The url of the site.
        **kwargs: max_length
    """

    url, name = get_img_name(url)
    url = url if url.startswith('http') else f'http:{url}'
    with open(name, 'wb') as f:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url, headers=headers) as res:
                data = await res.read()
                f.write(data)
                print(f'Saved {name}')


def async_save_imgs(urls:str):
    """
    Download images from links in an async style.
    """
    return [async_save_img(url) for url in urls]