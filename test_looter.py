import looter as lt
import requests
import pytest
import re


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
    assert type(r) == list and '#' not in r


@pytest.mark.ok
def test_re_links():
    res = lt.send_request(f'{domain}/post')
    hrefs = lt.re_links(res, r'https://konachan.net/wiki/.*?')
    assert type(hrefs) == list and len(hrefs) > 5


@pytest.mark.ok
def test_parse_robots():
    robots_url = lt.parse_robots(f'{domain}/post')
    assert type(robots_url) == list and len(robots_url) > 5


@pytest.mark.ok
def test_login():
    params = {'df': 'mail126_letter', 'from': 'web', 'funcid': 'loginone', 'iframe': '1', 'language': '-1', 'passtype': '1', 'product': 'mail126',
              'verifycookie': '-1', 'net': 'failed', 'style': '-1', 'race': '-2_-2_-2_db', 'uid': 'webscraping123@126.com', 'hid': '10010102'}
    postdata = {'username': 'webscraping123@126.com', 'savelogin': '1',
                'url2': 'http://mail.126.com/errorpage/error126.htm', 'password': '0up3VmfKCh22'}
    url = "https://mail.126.com/entry/cgi/ntesdoor?"
    res, ses = lt.login(url, postdata, params=params)
    index_url = re.findall(r'href = "(.*?)"', res.text)[0]
    index = ses.get(index_url)
    message_count = re.findall(
        r"('messageCount'.*?).*?('unreadMessageCount'.*?),", index.text)[0]
    assert message_count[0] == "'messageCount'"

# test utils

@pytest.mark.ok
def test_ensure_schema():
    assert lt.ensure_schema(domain).startswith('http')
    assert not lt.ensure_schema(f'http://{domain}').startswith('https')
    assert lt.ensure_schema('//fuckshit.png').startswith('https://')


@pytest.mark.ok
def test_get_domain():
    assert lt.get_domain(f'http://{domain}') == domain
    assert lt.get_domain(f'https://{domain}/post') == domain


@pytest.mark.ok
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


@pytest.mark.ok
def test_expand_num():
    assert lt.expand_num('61.8K') == 61800
    assert lt.expand_num('61.8M') == 61800000
    assert lt.expand_num('61.8') == 61.8
    assert lt.expand_num('61') == 61
