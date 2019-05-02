"""
简书上“程序员”专题下的文章
"""
from datetime import datetime
import looter as lt
import pymysql

domain = 'https://www.jianshu.com'
connection = pymysql.connect(
    host='localhost',
    db='techattic',
    charset='utf8mb4',
    user='test',
    password='test123')
cursor = connection.cursor()


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('ul.note-list li')
    for item in items:
        title = item.css('.content a.title::text').extract_first()
        author = item.css('a.nickname::text').extract_first()
        source = f"{domain}{item.css('.content a.title::attr(href)').extract_first()}"
        vote = max(map(int, (item.css('.meta span').re(r'\d+'))))
        site = 'jianshu'
        date = datetime.utcnow()
        view = 0
        comment = 0
        try:
            comment = int(item.css('.meta a::text').re_first(r'\d+'))
        except TypeError:
            pass
        collect = 0
        row = (title, author, source, vote, site, date, view, comment, collect)
        print(row)
        try:
            cursor.execute(
                'INSERT INTO `article` (`title`, `author`, `source`, `vote`, `site`, `date`, `view`, `comment`, `collect`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                row)
            connection.commit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    tasklist = [f'{domain}/c/NEt52a?order_by=top&page={n}' for n in range(1, 201)]
    result = [crawl(task) for task in tasklist]
    cursor.close()
    connection.close()
