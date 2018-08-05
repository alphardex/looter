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
import webbrowser
from operator import itemgetter
from http import cookiejar
import asyncio
from lxml import etree
from docopt import docopt
from .utils import *

VERSION = '1.84'

BANNER = """
Available objects:
    url           The url of the site you crawled.
    res           The response of the site.
    tree          The source tree, can be parsed by xpath and cssselect.

Available functions:
    fetch         Get the element tree of an HTML page. [has async version]
    view          View the page in your browser. (test rendering)
    save_imgs     Save the images you crawled. [has async version]
    alexa_rank    Get the reach and popularity of a site in alexa.
    links         Get all the links of the page.
    re_links      Get the links with a regex pattern.
    save_as_json  Save what you crawled as a json file.
    parse_robots  Parse the robots.txt of the site and retrieve its urls.
    login         Login the site using POST request, data required.

Examples:
    Crawl all the <li> items of a <ul> table:
        >>> items = tree.cssselect('ul li')

    Crawl images just in 1-line :d
        >>> save_imgs(links(res, search='jpg'))

For more info, plz refer to these sites:
    [looter]: https://github.com/alphardex/looter
    [cssselect]: http://www.runoob.com/cssref/css-selectors.html
    [xpath]: http://www.runoob.com/xpath/xpath-syntax.html
"""


def fetch(url: str, headers=None, proxies=None, use_cookies=False):
    """
    Get the element tree of an HTML page, use cssselect or xpath to parse it.

    Please refer to the tutorial of this module, and selector tutorial below:
        cssselect: http://www.runoob.com/cssref/css-selectors.html
        xpath: http://www.runoob.com/xpath/xpath-syntax.html

    Args:
        url (str): The url of the site.
        headers (optional): Defaults to fake-useragent, can be customed by user.
        proxies (optional): Defaults to None, can be customed by user.
        use_cookies (bool, optional): Defaults to False, if turn it on, paste document.cookie to a 'cookies.txt' file.

    Returns:
        The element tree of html.
    """
    cookies = read_cookies() if use_cookies else None
    res = send_request(url, headers=headers, proxies=proxies, cookies=cookies)
    if res:
        html = res.text
        tree = etree.HTML(html)
        return tree
    else:
        print('Failed to fetch the page.')


async def async_fetch(url: str, headers=None, proxies=None, use_cookies=False):
    """Fetch the element tree in an async style.

    Args:
        url (str): The url of the site.
        headers (optional): Defaults to fake-useragent, can be customed by user.
        proxies (optional): Defaults to None, can be customed by user.
        use_cookies (bool, optional): Defaults to False, if turn it on, paste document.cookie to a 'cookies.txt' file.

    Returns:
        The element tree of html.
    """
    cookies = read_cookies() if use_cookies else None
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url, headers=headers, proxies=proxies, cookies=cookies) as res:
            html = await res.text()
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


def save_imgs(urls, random_name=False, headers=None, proxies=None, cookies=None):
    """
    Download images from links.
    """
    return [save_img(url, random_name=random_name, headers=headers, proxies=proxies, cookies=cookies) for url in urls]


def async_save_imgs(urls: str, random_name=False, headers=None, proxies=None, cookies=None):
    """
    Download images from links in an async style.
    """
    loop = asyncio.get_event_loop()
    result = [async_save_img(url, random_name=random_name,
                             headers=headers, proxies=proxies, cookies=cookies) for url in urls]
    loop.run_until_complete(asyncio.wait(result))


def alexa_rank(url: str) -> tuple:
    """
    Get the reach and popularity of a site in alexa.

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


def links(res: requests.models.Response, search=None, absolute=False) -> list:
    """Get the links of the page.

    Args:
        res (requests.models.Response): The response of the page.
        search ([type], optional): Defaults to None. Search the links you want.
        absolute (bool, optional): Defaults to False. Get the absolute links.

    Returns:
        list: All the links of the page.
    """
    domain = ensure_schema(get_domain(res.url))
    tree = etree.HTML(res.text)
    hrefs = [link.get('href')
             for link in tree.cssselect('a') if link.get('href')]
    if search:
        hrefs = [href for href in hrefs if search in href]
    if absolute:
        hrefs = [f'{domain}{href}' for href in hrefs if not href.startswith('http')]
    hrefs = [href for href in hrefs if '#' not in href]
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
    hrefs = [href for href in hrefs if re.findall(pattern, href)]
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
    With this, maybe you are able to recursively crawl the site :)

    Args:
        url (str): The url of the site.

    Returns:
        list: The url list of the robots.txt.
    """
    domain = get_domain(ensure_schema(url))
    res = send_request(f'{domain}/robots.txt')
    if res:
        matches = re.findall(r'Allow: (.*)|Disallow: (.*)', res.text)
        if matches:
            matches = [''.join(match) for match in matches]
            robots_urls = [
                f'https://{domain}{match}' for match in matches if '*' not in match]
            print(f'URLs retrieved from robots.txt: {len(robots_urls)}')
            return robots_urls
    else:
        print('Parse failed, plz ensure that the url is a valid one.')


def login(url: str, data: dict, headers: dict=None, params: dict=None, use_cookies=False) -> tuple:
    """Login the site using POST request, data required.

    Args:
        url (str): The login_page url of the site.
        data (dict): The POST request form data.
        headers (dict, optional): Defaults to fake-useragent, can be customed by user.
        params (dict, optional): Defaults to {}, can be customed by user.
        use_cookies (bool, optional): Defaults to False, use cookies to login (needs a 'cookies.txt' file)

    Returns:
        tuple: If succeeded, the response and session will be returned to access the site.
    """
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    session = requests.Session()
    if use_cookies:
        session.cookies = read_cookies()
    try:
        res = session.post(url, data=data, headers=headers, params=params)
        print(res.status_code)
        print(res.text)
        return res, session
    except Exception as e:
        print(f'[Err] {e}')


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
            template = f'{template}_async'
        package_path = os.path.dirname(__file__)
        with open(f'{package_path}\\templates\\{template}.tmpl', 'r') as i, open(f'{name}.py', 'w') as o:
            o.write(i.read())

    if argv['shell']:
        if not argv['<url>']:
            url = input('Which site do u want to crawl?\nurl: ')
        else:
            url = argv['<url>']
        res = send_request(url)
        if not res:
            exit('Failed to fetch the page.')
        tree = etree.HTML(res.text)
        allvars = {**locals(), **globals()}
        try:
            from ptpython.repl import embed
            print(BANNER)
            embed(allvars)
        except ImportError:
            code.interact(local=allvars, banner=BANNER)


if __name__ == '__main__':
    cli()
