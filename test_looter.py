import looter as lt
import requests
import pytest


domain = 'konachan.net'

# test main functions (excluding async and io functions, which can be tested through running examples)


@pytest.mark.ok
def test_fetch():
    tree = lt.fetch(f'{domain}/post')
    imgs = tree.cssselect('a.directlink')
    assert len(imgs) > 0


@pytest.mark.ok
def test_alexa_rank():
    r = lt.alexa_rank(domain)
    assert type(r) == tuple and len(r) == 3


@pytest.mark.ok
def test_links():
    res = lt.send_request(domain)
    r = lt.links(res)
    assert type(r) == list


@pytest.mark.ok
def test_re_links():
    res = lt.send_request(f'{domain}/post')
    hrefs = lt.re_links(res, r'http://konachan.net/wiki/.*?')
    assert type(hrefs) == list and len(hrefs) > 5


@pytest.mark.ok
def test_parse_robots():
    robots_url = lt.parse_robots(f'{domain}/post')
    assert type(robots_url) == list and len(robots_url) > 5


# test utils

@pytest.mark.ok
def test_ensure_schema():
    assert lt.ensure_schema(domain).startswith('http')
    assert not lt.ensure_schema(f'http://{domain}').startswith('https')


@pytest.mark.ok
def test_get_domain():
    assert lt.get_domain(f'http://{domain}') == f'http://{domain}'
    assert lt.get_domain(f'https://{domain}/post') == f'http://{domain}'


def test_send_request():
    res = lt.send_request(domain)
    assert type(res) == requests.models.Response
    assert res.status_code == 200


@pytest.mark.ok
def test_rectify():
    name = '?sdad<>:4rewr?'
    r = lt.rectify(name)
    assert r == 'sdad4rewr'


@pytest.mark.ok
def test_get_img_info():
    tree = lt.fetch(f'{domain}/post')
    img = tree.cssselect('a.directlink')[0]
    url, name = lt.get_img_info(img)
    assert url == img.get('href') and '%' not in name
