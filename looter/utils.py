import requests


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
