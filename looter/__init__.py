"""Looter, a python package designed for web crawler lovers :)
Author: alphardex  QQ:2582347430
If any suggestion, please contact me.
Thank you for cooperation!

Usage:
  looter genspider <name> [--async]
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
from itertools import groupby
from pathlib import Path
import tempfile
import requests
import aiohttp
from parsel import Selector
from docopt import docopt
from boltons.urlutils import find_all_links

VERSION = '2.16'
DEFAULT_HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
BANNER = """
Available objects:
    url           The url of the site you crawled.
    res           The response of the site.
    tree          The element source tree to be parsed.

Available functions:
    fetch         Send HTTP request to the site and parse it as a tree. [has async version]
    view          View the page in your browser. (test rendering)
    links         Get the links of the page.
    save_as_json  Save what you crawled as a json file.

Examples:
    Get all the <li> elements of a <ul> table:
        >>> items = tree.css('ul li')

    Get the links with a regex pattern:
        >>> items = links(res, pattern=r'.*/(jpeg|image)/.*')

For more info, plz refer to documentation:
    [looter]: https://looter.readthedocs.io/en/latest/
"""


def fetch(url: str, **kwargs) -> Selector:
    """
    Send HTTP request and parse it as a DOM tree.

    Args:
        url (str): The url of the site.

    Returns:
        Selector: allows you to select parts of HTML text using CSS or XPath expressions.
    """
    kwargs.setdefault('headers', DEFAULT_HEADERS)
    try:
        res = requests.get(url, **kwargs)
        res.raise_for_status()
    except requests.RequestException as e:
        print(e)
    else:
        html = res.text
        tree = Selector(text=html)
        return tree


async def async_fetch(url: str, **kwargs) -> Selector:
    """
    Do the fetch in an async style.

    Args:
        url (str): The url of the site.

    Returns:
        Selector: allows you to select parts of HTML text using CSS or XPath expressions.
    """
    kwargs.setdefault('headers', DEFAULT_HEADERS)
    async with aiohttp.ClientSession(**kwargs) as ses:
        async with ses.get(url, **kwargs) as res:
            html = await res.text()
            tree = Selector(text=html)
            return tree


def view(url: str, **kwargs) -> bool:
    """
    View the page whether rendered properly. (ensure the <base> tag to make external links work)

    Args:
        url (str): The url of the site.
    """
    kwargs.setdefault('headers', DEFAULT_HEADERS)
    html = requests.get(url, **kwargs).content
    if b'<base' not in html:
        repl = f'<head><base href="{url}">'
        html = html.replace(b'<head>', repl.encode('utf-8'))
    fd, fname = tempfile.mkstemp('.html')
    os.write(fd, html)
    os.close(fd)
    return webbrowser.open(f'file://{fname}')


def links(res: requests.models.Response,
          search: str = None,
          pattern: str = None) -> list:
    """Get the links of the page.

    Args:
        res (requests.models.Response): The response of the page.
        search (str, optional): Defaults to None. Search the links you want.
        pattern (str, optional): Defaults to None. Search the links use a regex pattern.

    Returns:
        list: All the links of the page.
    """
    hrefs = [link.to_text() for link in find_all_links(res.text)]
    if search:
        hrefs = [href for href in hrefs if search in href]
    if pattern:
        hrefs = [href for href in hrefs if re.findall(pattern, href)]
    return list(set(hrefs))


def save_as_json(total: list,
                 name='data.json',
                 sort_by: str = None,
                 no_duplicate=False,
                 order='asc'):
    """Save what you crawled as a json file.

    Args:
        total (list): Total of data you crawled.
        name (str, optional): Defaults to 'data.json'. The name of the file.
        sort_by (str, optional): Defaults to None. Sort items by a specific key.
        no_duplicate (bool, optional): Defaults to False. If True, it will remove duplicated data.
        order (str, optional): Defaults to 'asc'. The opposite option is 'desc'.
    """
    if sort_by:
        reverse = order == 'desc'
        total = sorted(total, key=itemgetter(sort_by), reverse=reverse)
    if no_duplicate:
        total = [key for key, _ in groupby(total)]
    data = json.dumps(total, ensure_ascii=False)
    Path(name).write_text(data, encoding='utf-8')


def cli():
    """
    Commandline for looter :d
    """
    argv = docopt(__doc__, version=VERSION)
    if argv['genspider']:
        name = f"{argv['<name>']}.py"
        use_async = argv['--async']
        template = 'data_async.tmpl' if use_async else 'data.tmpl'
        package_dir = Path(__file__).parent
        template_text = package_dir.joinpath('templates', template).read_text()
        Path(name).write_text(template_text)
    if argv['shell']:
        url = argv['<url>'] if argv['<url>'] else input(
            'Plz specific a site to crawl\nurl: ')
        res = requests.get(url, headers=DEFAULT_HEADERS)
        if not res:
            exit('Failed to fetch the page.')
        tree = Selector(text=res.text)
        allvars = {**locals(), **globals()}
        try:
            from ptpython.repl import embed
            print(BANNER)
            embed(allvars)
        except ImportError:
            code.interact(local=allvars, banner=BANNER)


if __name__ == '__main__':
    cli()
