import os
import time
import uuid
import functools
from urllib.parse import unquote, urlparse
import requests
import aiohttp
from fake_useragent import UserAgent


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


def ensure_schema(url: str) -> str:
    """Ensure the url starts with a https schema.

    Args:
        url (str): A url without https schema such as konachan.com.

    Returns:
        str: A url with https schema such as https://konachan.com.
    """
    if url.startswith('http'):
        return url
    else:
        return f'https:{url}' if url.startswith('//') else f'https://{url}'


def get_domain(url: str) -> str:
    """Get the domain(hostname) of the site.

    Args:
        url (str): A url with http schema.

    Returns:
        str: the domain(hostname) of the site.
    """
    return urlparse(url).netloc


def send_request(url: str, timeout=60, headers=None, proxies=None, cookies=None) -> requests.models.Response:
    """Send an HTTP request to a url.

    Args:
        url (str): The url of the site.
        timeout (int, optional): Defaults to 60. The maxium time of request.
        headers (optional): Defaults to fake-useragent, can be customed by user.
        proxies (optional): Defaults to None, can be customed by user.
        cookies (optional): Defaults to None, if needed, use read_cookies().

    Returns:
        requests.models.Response: The response of the HTTP request.
    """
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    url = ensure_schema(url)
    try:
        res = requests.get(url, headers=headers, timeout=timeout, proxies=proxies, cookies=cookies)
        res.raise_for_status()
    except Exception as e:
        print(f'[Err] {e}')
    else:
        return res


def rectify(name: str) -> str:
    """
    Get rid of illegal symbols of a filename.

    Args:
        name (str): The filename.

    Returns:
        The rectified filename.
    """
    name = ''.join([c for c in unquote(name) if c not in {
                   '?', '<', '>', '|', '*', '"', ":"}])
    return name


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
    name = ensure_schema(url).split('/')[-1]
    fname, ext = rectify(name).rsplit('.', 1)
    name = f'{fname[:max_length]}.{ext}'
    return url, name


@perf
def save_img(url: str, random_name=False, headers=None, proxies=None, cookies=None):
    """
    Download image and save it to local disk.

    Args:
        url (str): The url of the site.
        random_name (int, optional): Defaults to False. If names of images are duplicated, use this.
        headers (optional): Defaults to fake-useragent, can be customed by user.
        proxies (optional): Defaults to None, can be customed by user.
        cookies (optional): Defaults to None, if needed, use read_cookies().
    """
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    url, name = get_img_info(url)
    if random_name:
        fname, ext = os.path.splitext(name)
        name = f'{fname}{str(uuid.uuid1())[:8]}{ext}'
    with open(name, 'wb') as f:
        f.write(send_request(url, headers=headers, proxies=proxies, cookies=cookies).content)
        print(f'Saved {name}')


async def async_save_img(url: str, random_name=False, headers=None, proxy=None, cookies=None):
    """Save an image in an async style.

    Args:
        url (str): The url of the site.
        random_name (int, optional): Defaults to False. If names of images are duplicated, use this.
        headers (optional): Defaults to fake-useragent, can be customed by user.
        proxy (optional): Defaults to None, can be customed by user.
        cookies (optional): Defaults to None, if needed, use read_cookies().
    """
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    url, name = get_img_info(url)
    if random_name:
        fname, ext = os.path.splitext(name)
        name = f'{fname}{str(uuid.uuid1())[:8]}{ext}'
    with open(name, 'wb') as f:
        async with aiohttp.ClientSession(cookies=cookies) as ses:
            async with ses.get(url, headers=headers, proxy=proxy) as res:
                data = await res.read()
                f.write(data)
                print(f'Saved {name}')


def expand_num(num: str) -> int:
    """Expand the number abbr to the actual one.

    Args:
        number (str): The number to expand, e.g.: 61.8K, 78.4M

    Returns:
        int: The expanded number.
    """
    num = num.lower()
    abbrs = {'k': 1000, 'm': 1000000}
    if num[-1] in abbrs.keys():
        return int(float(num[:-1]) * abbrs.get(num[-1]))
    else:
        return float(num) if '.' in num else int(num)


def read_cookies(filename: str='cookies.txt') -> requests.cookies.RequestsCookieJar:
    """Read cookies from a 'cookies.txt' file, which can be created from document.cookie.

    Args:
        filename (str): Defaults to 'cookies.txt'.

    Returns:
        requests.cookies.RequestsCookieJar: A cookiejar object that can be passed to cookies param.
    """
    jar = requests.cookies.RequestsCookieJar()
    with open(filename) as f:
        cookies = f.read()
        for cookie in cookies.split(';'):
            name, value = cookie.strip().split('=', 1)
            jar.set(name, value)
        return jar
