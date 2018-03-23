""" Looter, a python package designed for web crawler lovers :)
Author: alphardex  QQ:2582347430
If any suggestion, please contact me. 
Thank you for cooperation!

Usage:
  looter genspider <name> <tmpl>
  looter shell [<url>]
  looter (-h | --help | --version)

Options:
  -h --help        Show this screen.
  --version        Show version.
"""
import os
import code
import re
import time
import random
import webbrowser
import functools
from urllib.parse import unquote
import aiohttp
import requests
from lxml import etree
from fake_useragent import UserAgent
from docopt import docopt

VERSION = '1.51'
UA = UserAgent()
HEADERS = {'User-Agent': UA.random}

BANNER = f"""
Available objects:
    url          The url of the site you crawled.
    res          The response of the site.
    tree         The source tree, can be parsed by xpath and cssselect.

Available functions:
    fetch        Get the element tree of an HTML page.
    view         View the page in your browser. (test rendering)
    links        Get all the links of the page.
    save_imgs    Download images from links.
    alexa_rank   Get the reach and popularity of a site in alexa.

For more info, plz refer to tutorial:
    [cssselect]: http://www.runoob.com/cssref/css-selectors.html
    [xpath]: http://www.runoob.com/xpath/xpath-syntax.html
"""


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


def send_request(url: str, **kwargs) -> requests.models.Response:
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
        res = requests.get(url, headers=HEADERS, timeout=timeout)
        res.raise_for_status()
    except requests.exceptions.MissingSchema:
        res = requests.get('http://' + url, headers=HEADERS, timeout=timeout)
    return res


def fetch(url: str, **kwargs):
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


def view(url: str, **kwargs):
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


def rectify(name: str) -> str:
    """
    Get rid of illegal symbols of a filename.

    Args:
        name: The filename.

    Returns:
        The rectified filename.
    """
    if any(symbol in name for symbol in ['?', '<', '>', '|', '*', '"', ":"]):
        name = ''.join([c for c in name if c not in {
            '?', '<', '>', '|', '*', '"', ":"}])
    return unquote(name)


def get_img_name(url: str, **kwargs) -> str:
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
def save_img(url: str, random_name=False):
    """
    Download image and save it to local disk.

    Args:
        url: The url of the site.
        random_name: If names of images is duplicated, use this.
    """
    url, name = get_img_name(url)
    if random_name:
        name = f'{name[:-4]}{str(random.randint(1, 1000000))}{name[-4:]}'
    with open(name, 'wb') as f:
        url = url if url.startswith('http') else f'http:{url}'
        f.write(requests.get(url, headers=HEADERS).content)
        print(f'Saved {name}')


def save_imgs(urls, random_name=False):
    """
    Download images from links.
    """
    return [save_img(url, random_name=random_name) for url in urls]


def alexa_rank(url: str) -> tuple:
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
    reach_rank = re.findall(r'REACH[^\d]*(\d+)', page)
    popularity_rank = re.findall(r'POPULARITY[^\d]*(\d+)', page)
    if reach_rank and popularity_rank:
        print(f'[{url}] REACH: {reach_rank[0]} POPULARITY: {popularity_rank[0]}')
        return url, reach_rank[0], popularity_rank[0]
    else:
        print(f'[{url}] Get rank failed.')
        return None


async def async_fetch(url: str, **kwargs):
    """Fetch a webpage in an async style.

    Args:
        url: The url of the site.
        **kwargs: type

    Returns:
        The element tree of the HTML page.
    """
    type_ = kwargs.get('type', 'text')
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url, headers=HEADERS) as res:
            html = await res.text() if type_ == 'text' else res.read()
            tree = etree.HTML(html)
            return tree


async def async_save_img(url: str, random_name=False):
    """Save an image in an async style.

    Args:
        url: The url of the site.
        random_name: If names of images is duplicated, use this.
    """

    url, name = get_img_name(url)
    url = url if url.startswith('http') else f'http:{url}'
    if random_name:
        name = f'{name[:-4]}{str(random.randint(1, 1000000))}{name[-4:]}'
    with open(name, 'wb') as f:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url, headers=HEADERS) as res:
                data = await res.read()
                f.write(data)
                print(f'Saved {name}')


def async_save_imgs(urls: str, random_name=False):
    """
    Download images from links in an async style.
    """
    return [async_save_img(url, random_name=random_name) for url in urls]


def links(res: requests.models.Response, search=None, absolute=False) -> list:
    """Get all the links of the page.

    Args:
        res: The response of the page.
        search: Search the links you want.  (default: {None})
        absolute: Get the absolute links.   (default: {False})

    Returns:
        All the links of the page.
    """
    domain = res.url
    tree = etree.HTML(res.text)
    hrefs = [link.get('href')
             for link in tree.cssselect('a') if link.get('href')]
    if search:
        hrefs = [href for href in hrefs if search in href]
    if absolute:
        hrefs = [domain + href for href in hrefs if not href.startswith('http')]
    return hrefs


def cli():
    """
    Commandline for looter!
    """
    argv = docopt(__doc__, version=VERSION)
    if argv['genspider']:
        template = argv['<tmpl>']
        name = argv['<name>']
        if template not in ['data', 'image', 'async']:
            exit('Plz provide a template (data, image or async)')
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
        code.interact(local=allvars, banner=BANNER)


if __name__ == '__main__':
    cli()