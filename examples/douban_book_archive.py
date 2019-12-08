"""
我看过的书籍在豆瓣上的归档
"""
import looter as lt

domain = 'https://book.douban.com'
MAX_PAGE = 4
cookie = 'll="108169"; bid=uRkL12JXzhg; gr_user_id=59ffc171-7ba8-45d4-9848-d04cae3b99cc; _vwo_uuid_v2=DB7C868DC8A7D64AC4F5CA5FABCD30D38|4602ea9fbee2cc9464c993b2583c33b2; __yadk_uid=F3jytnOVCtD1iSsRYhBQoJCWnYu4LlvH; __gads=ID=15a1f5c9d2c8e1c1:T=1565230512:S=ALNI_MbiSb0-9zzDosCeLic43kt9Wajqxw; douban-profile-remind=1; __utmv=30149280.15853; viewed="26349497_25909351_25920727_30170670_25872086_30386804_30239781_4279678_2280547_1139336"; push_noty_num=0; push_doumail_num=0; __utmz=81379588.1575535591.31.25.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/158535797/; __utmz=30149280.1575727536.50.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1575772677%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F158535797%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.535054538.1565077784.1575727536.1575772677.51; __utmc=30149280; __utmt_douban=1; __utmc=81379588; __utma=81379588.2002100436.1565077801.1575535591.1575772677.32; __utmt=1; dbcl2="158535797:Ox8dyd/5hW4"; ck=SDvR; __utmt=1; _pk_id.100001.3ac3=6a5ac498d3bf471e.1565077801.32.1575772866.1575536822.; __utmb=30149280.9.10.1575772677; __utmb=81379588.7.10.1575772677'
headers = lt.DEFAULT_HEADERS
headers['Cookie'] = cookie


def crawl(url):
    tree = lt.fetch(url, headers=headers)
    items = tree.css('.list-view .item')
    for item in items:
        data = {}
        data['title'] = item.css('a::text').extract_first().strip()
        data['url'] = item.css('a::attr(href)').extract_first().strip()
        intro = item.css('span.intro::text').extract_first()
        data['date'] = intro.split('/')[-2].strip()
        data['intro'] = intro
        yield data


if __name__ == '__main__':
    tasklist = [f'{domain}/people/158535797/collect?sort=time&start=0&filter=all&mode=list&tags_sort=count']
    total = lt.crawl_all(crawl, tasklist)
    lt.save(total, name='douban_book_archive.csv')
