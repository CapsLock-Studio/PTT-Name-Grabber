# coding=utf-8
import sys
import os
import requests
import re
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')

index = 'https://www.ptt.cc/'
base_path = index + 'bbs/%s/index%s.html'


def content_parser(content):
    result = []
    tree = pq(content)
    author = tree('.article-metaline .article-meta-value').eq(0).text()
    result.append(author)
    pusher = tree('.push .push-userid')
    for user in pusher.items():
        result.append(user.text())
    return result


def query(board, regex, from_page, to_page):
    result = []
    from_page = int(from_page)
    to_page = int(to_page)
    for page in range(from_page, to_page + 1):
        res = requests.get(base_path % (board, page), cookies=dict(over18='1'))
        res.encoding = 'utf-8'
        if res.status_code < 400:
            tree = pq(res.text)
            elements = tree('.title>a')
            for ele in elements.items():
                title = ele.text().strip()
                if re.search(regex.decode('utf-8'), title, re.UNICODE):
                    url = ele.attr('href')
                    ids = content_parser(requests.get(index + url).text)
                    for data in ids:
                        if data not in result:
                            result.append(data)
        else:
            continue
    print result


if __name__ == '__main__':
    if len(sys.argv) >= 4:
        query(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print 'Usage: %s [board] [regex] [from_page] [to_page]' % os.path.abspath(__file__)
