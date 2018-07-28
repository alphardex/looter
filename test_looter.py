import looter as lt
import pytest


domain = 'konachan.net/post'


@pytest.mark.ok
def test_get():
    res = lt.send_request(domain)
    assert res.status_code == 200


@pytest.mark.ok
def test_fetch():
    tree = lt.fetch(domain)
    imgs = tree.cssselect('a.directlink')
    assert len(imgs) > 0


@pytest.mark.ok
def test_rectify():
    name = '?sdad<>:4rewr?'
    r = lt.rectify(name)
    assert r == 'sdad4rewr'


@pytest.mark.ok
def test_alexa_rank():
    r = lt.alexa_rank(domain)
    assert type(r) == tuple


@pytest.mark.ok
def test_links():
    res = lt.send_request(domain)
    r = lt.links(res)
    assert type(r) == list


@pytest.mark.ok
def test_re_links():
    res = lt.send_request('http://www.spbeen.com')
    hrefs = lt.re_links(res,'https?://www.spbeen.com//p/.*?')
    assert type(hrefs) == list


@pytest.mark.ok
def test_absolute_links():
    res = lt.send_request('http://www.spbeen.com')
    hrefs = [href.replace('http://','') for href in lt.links(res, absolute=True)]
    assert len([href for href in hrefs if "//" in href])==0

