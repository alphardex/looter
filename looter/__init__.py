"""Looter, a python package designed for web crawler lovers :)
Author: alphardex  QQ:2582347430
If any suggestion, please contact me. 
Thank you for cooperation!

Usage:
  looter genspider <name> <tmpl> [--async]
  looter shell [<url>]
  looter (-h | --help | --version)

Options:
  -h --help        Show this screen.
  --version        Show version.
  --async          Use async instead of concurrent.
"""
import os
import json
import code
import re
import time
import uuid
import random
import webbrowser
import functools
from operator import itemgetter
from urllib.parse import unquote
import asyncio
import aiohttp
import requests
from lxml import etree
from fake_useragent import UserAgent
from docopt import docopt

VERSION = '1.68'

BANNER = """
Available objects:
    url           The url of the site you crawled.
    res           The response of the site.
    tree          The source tree, can be parsed by xpath and cssselect.

Available functions:
    fetch         Get the element tree of an HTML page.
    view          View the page in your browser. (test rendering)
    links         Get all the links of the page.
    re_links      Get the links with a regex pattern.
    alexa_rank    Get the reach and popularity of a site in alexa.
    save_imgs     Save the images you crawled.
    save_as_json  Save what you crawled as a json file.
    parse_robots  Parse the robots.txt of the site and retrieve its urls.

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


def send_request(url: str, timeout=60, use_proxies=False, headers=None) -> requests.models.Response:
    """Send an HTTP request to a url.
    
    Args:
        url (str): The url of the site.
        timeout (int, optional): Defaults to 60. The maxium time of request.
        headers (optional): Defaults to fake-useragent, can be customed by user.

    Returns:
        requests.models.Response: The response of the HTTP request.
    """
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        res.raise_for_status()
    except requests.exceptions.MissingSchema:
        res = requests.get('http://' + url, headers=headers, timeout=timeout, proxies=proxies)
    return res


def fetch(url: str, headers=None):
    """
    Get the element tree of an HTML page, use cssselect or xpath to parse it.

    Please refer to the tutorial of this module, and selector tutorial below:
        cssselect: http://www.runoob.com/cssref/css-selectors.html
        xpath: http://www.runoob.com/xpath/xpath-syntax.html

    Args:
        url (str): The url of the site.
        headers (optional): Defaults to fake-useragent, can be customed by user.
    
    Returns:
        The element tree of html.
    """
    res = send_request(url, headers=headers)
    html = res.text
    tree = etree.HTML(html)
    return tree


def view(url: str, encoding='utf-8', name='test'):
    """
    View the page whether rendered properly. (Usually for testing purpose)

    Args:
        url (str): The url of the site.
        encoding (str, optional): Defaults to 'utf-8'. The encoding of the file.
        name (str, optional): Defaults to 'test'. The name of the file.
    """
    with open(f'{name}.html', 'w', encoding=encoding) as f:
        f.write(send_request(url).text)
    webbrowser.open(f'{name}.html', new=1)


def rectify(name: str) -> str:
    """
    Get rid of illegal symbols of a filename.

    Args:
        name (str): The filename.

    Returns:
        The rectified filename.
    """
    name = ''.join([c for c in name if c not in {'?', '<', '>', '|', '*', '"', ":"}])
    return unquote(name)


def get_img_info(url: str, max_length=160) -> tuple:
    """Get the info of an image.

    Args:
        url (str): The url of the site.
        max_length (int, optional): Defaults to 160. The maximal length of the filename.

    Returns:
        tuple: The url of an image and its name.
    """
    if hasattr(url, 'tag') and url.tag == 'a':
        url = url.get('href')
    elif hasattr(url, 'tag') and url.tag == 'img':
        url = url.get('src')
    url = url if url.startswith('http') else f'http:{url}'
    name = rectify(url.split('/')[-1])
    ext = name.split('.')[-1]
    name = f"{name[:max_length]}.{ext}"
    name = name[:-4] if name.endswith(f'.{ext}.{ext}') else name
    return url, name


@perf
def save_img(url: str, random_name=False):
    """
    Download image and save it to local disk.

    Args:
        url (str): The url of the site.
        random_name (int, optional): Defaults to False. If names of images are duplicated, use this.
    """
    url, name = get_img_info(url)
    if random_name:
        name = f'{name[:-4]}{str(uuid.uuid1())[:8]}{name[-4:]}'
    with open(name, 'wb') as f:
        f.write(send_request(url).content)
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
        url (str): The url of the site.

    Returns:
        tuple: (url, reach_rank, popularity_rank)
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


async def async_fetch(url: str, headers=None):
    """Fetch the element tree in an async style.

    Args:
        url (str): The url of the site.
        headers (optional): Defaults to fake-useragent, can be customed by user.

    Returns:
        The element tree of html.
    """
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url, headers=headers) as res:
            html = await res.text()
            tree = etree.HTML(html)
            return tree


async def async_save_img(url: str, random_name=False):
    """Save an image in an async style.

    Args:
        url (str): The url of the site.
        random_name (int, optional): Defaults to False. If names of images are duplicated, use this.
    """
    headers = {'User-Agent': UserAgent().random}
    url, name = get_img_info(url)
    if random_name:
        name = f'{name[:-4]}{str(uuid.uuid1())[:8]}{name[-4:]}'
    with open(name, 'wb') as f:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url, headers=headers) as res:
                data = await res.read()
                f.write(data)
                print(f'Saved {name}')


def async_save_imgs(urls: str, random_name=False):
    """
    Download images from links in an async style.
    """
    loop = asyncio.get_event_loop()
    result = [async_save_img(url, random_name=random_name) for url in urls]
    loop.run_until_complete(asyncio.wait(result))


def links(res: requests.models.Response, search=None, absolute=False) -> list:
    """Get all the links of the page.
    
    Args:
        res (requests.models.Response): The response of the page.
        search ([type], optional): Defaults to None. Search the links you want.
        absolute (bool, optional): Defaults to False. Get the absolute links.
    
    Returns:
        list: All the links of the page.
    """
    domain = res.url
    tree = etree.HTML(res.text)
    hrefs = [link.get('href')
             for link in tree.cssselect('a') if link.get('href')]
    if search:
        hrefs = [href for href in hrefs if search in href]
    if absolute:
        hrefs = [domain[:-1] + href for href in hrefs if not href.startswith('http')]
    return hrefs


def re_links(res: requests.models.Response, pattern: str) -> list:
    """Get the links using regex pattern.
    
    Args:
        res (requests.models.Response): The response of the page.
        pattern (str): Regular expression.

    Returns:
        list: Links that match the rules.
    """
    hrefs = links(res, absolute=True)
    hrefs = [href for href in hrefs if re.findall(pattern,href)]
    return hrefs


def save_as_json(total: list, name='data', sort_by=None):
    """Save what you crawled as a json file.
    
    Args:
        total (list): Total of data you crawled.
        name (str, optional): Defaults to 'data'. The name of the json file.
        sort_by ([type], optional): Defaults to None. Sort items by a specific key.
    """
    if sort_by:
        total = sorted(total, key=itemgetter(sort_by))
    with open(f'{name}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(total, ensure_ascii=False))


def parse_robots(url: str) -> list:
    """Parse the robots.txt of the site and retrieve its urls.
    
    Args:
        url (str): The url of the site.
    
    Returns:
        list: The url list of the robots.txt.
    """
    res = send_request(f'{url}/robots.txt')
    if res.status_code != 404:
        matches = re.findall(r'Allow: (.*)|Disallow: (.*)', res.text)
        if matches:
            matches = [''.join(match) for match in matches]
            robots_urls = [f'{url}{match}' for match in matches if '*' not in match]
            print(f'URLs retrieved from robots.txt: {len(robots_urls)}')
            return robots_urls
    else:
        print('Parse failed, make sure url is the hostname, not the path!')


def cli():
    """
    Commandline for looter!
    """
    argv = docopt(__doc__, version=VERSION)
    if argv['genspider']:
        template = argv['<tmpl>']
        name = argv['<name>']
        async_ = argv['--async']
        if template not in ['data', 'image']:
            exit('Plz provide a template (data, image)')
        if async_:
            template = template + '_async'
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
