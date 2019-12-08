"""
Looter, Web-Scraping for Humans.

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
import webbrowser
from operator import itemgetter
from itertools import groupby
from concurrent import futures
from pathlib import Path
from typing import Callable
import tempfile
import requests
import aiohttp
from parsel import Selector
from docopt import docopt
from tqdm import tqdm

VERSION = '2.21'
DEFAULT_HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
DEFAULT_ENCODING = 'utf-8'
BANNER = """
Available objects:
    url           The url of the site.
    res           The response of the site.
    tree          The DOM selector tree.

Available functions:
    fetch         Send HTTP request and parse it as a DOM selector. [has async version]
    view          View the page in your browser. (test rendering)
    save          Save what you crawled as a file. (json or csv)

Examples:
    Get all the <li> elements of a <ul> table:
        >>> items = tree.css('ul li').extract()

    Get all the links of a page:
        >>> items = tree.css('a::attr(href)').extract()

For more info, plz refer to documentation:
    [looter]: https://looter.readthedocs.io/en/latest/
"""


def fetch(url: str, **kwargs) -> Selector:
    """
    Send HTTP request and parse it as a DOM selector.

    Args:
        url (str): The url of the site.

    Returns:
        Selector: allows you to select parts of HTML text using CSS or XPath expressions.
    """
    kwargs.setdefault('headers', DEFAULT_HEADERS)
    try:
        res = requests.get(url, **kwargs)
        res.encoding = kwargs.get('encoding', DEFAULT_ENCODING)
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
    if b'<base' not in (html := requests.get(url, **kwargs).content):
        html = html.replace(b'<head>', f'<head><base href={url}>'.encode('utf-8'))
    fd, fname = tempfile.mkstemp('.html')
    os.write(fd, html)
    os.close(fd)
    return webbrowser.open(f'file://{fname}')


def save(total: list, *, name='data.json', sort_by: str = None, no_duplicate=False, order='asc'):
    """
    Save what you crawled as a file, default format is json.

    Args:
        total (list): Total of data you crawled.
        name (str, optional): Defaults to 'data.json'. The name of the file.
        sort_by (str, optional): Defaults to None. Sort items by a specific key.
        no_duplicate (bool, optional): Defaults to False. If True, it will remove duplicated data.
        order (str, optional): Defaults to 'asc'. The opposite option is 'desc'.
    """
    if sort_by:
        total = sorted(total, key=itemgetter(sort_by), reverse=order == 'desc')
    if no_duplicate:
        total = [key for key, _ in groupby(total)]
    _, ext = name.split('.')
    if ext == 'json':
        data = json.dumps(total, ensure_ascii=False)
        Path(name).write_text(data, encoding='utf-8')
    elif ext == 'csv':
        try:
            import pandas as pd
            pd.DataFrame(total).to_csv(name, encoding='utf-8')
        except ImportError:
            exit('pandas not installed! Plz run `pip install pandas`.')
    else:
        exit('Sorry, other formats are not supported yet.')


def crawl_all(crawl: Callable, tasklist: list, max_workers=50) -> list:
    """
    Crawl all the tasks in a tasklist.

    Args:
        crawl (Callable): The "crawl" function.
        tasklist (list): A list of url.
        max_workers (int, optional): Max thread count. Defaults to 50.

    Returns:
        list: Total of data you crawled.
    """
    with futures.ThreadPoolExecutor(max_workers) as executor:
        fs = {executor.submit(crawl, task): task for task in tasklist}
        completed = futures.as_completed(fs)
        completed = tqdm(completed, total=len(tasklist))
        total = []
        for future in completed:
            task = fs[future]
            try:
                result = future.result()
            except Exception as e:
                print(f'[{e}] {task}.')
            else:
                if result:
                    total.extend(list(result))
        return total


def cli():
    """
    Commandline for looter :d
    """
    argv = docopt(__doc__, version=VERSION)
    if argv['genspider']:
        template = 'data_async.tmpl' if argv['--async'] else 'data.tmpl'
        template_path = Path(__file__).parent / 'templates' / template
        Path(f"{argv['<name>']}.py").write_text(template_path.read_text())
    if argv['shell']:
        url = argv['<url>'] if argv['<url>'] else input('Specify the url: ')
        res = requests.get(url, headers=DEFAULT_HEADERS)
        res.encoding = DEFAULT_ENCODING
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
