# coding:utf-8
import time
import execjs
import requests
from lxml.html import etree

with open('demo.js', encoding="utf-8") as f:
    js_text = f.read()
    js = execjs.compile(js_text)


def get_cookie():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    url = 'http://app1.cfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604'
    with requests.get(url, headers=headers) as r:
        r.raise_for_status()
        root = etree.HTML(r.text)
        meta = root.xpath('//meta[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
        f82s = r.cookies.get('FSSBBIl1UgzbN7N80S')
    f82t = js.call('make_cookie', meta)
    print(f82t)
    cookie = f"FSSBBIl1UgzbN7N80S={f82s}; FSSBBIl1UgzbN7N80T={f82t}"
    print(cookie)
    return cookie


def get_list(cookie):
    url = 'http://app1.cfda.gov.cn/datasearchcnda/face3/search.jsp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        "Cookie": cookie,
    }
    data = {
        "tableId": "25",
        "bcId": "152904713761213296322795806604",
        "tableName": "TABLE25",
        "viewtitleName": "COLUMN167",
        "viewsubTitleName": "COLUMN821,COLUMN170,COLUMN166",
        "curstart": "1",
        "tableView": "%E5%9B%BD%E4%BA%A7%E8%8D%AF%E5%93%81",
    }
    with requests.post(url, headers=headers, data=data) as req:
        print(req.status_code)
        print(req.text)


def get_info(cookie, uid='73911'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        "Cookie": cookie,
        'Referer': 'http://app1.cfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604',
    }

    url = f'http://app1.cfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%B9%FA%B2%FA%D2%A9%C6%B7&Id={uid}'
    with requests.get(url, headers=headers) as req:
        req.raise_for_status()
        print(req.status_code, url)
        print(req.text)


if __name__ == '__main__':
    cookie = get_cookie()
    get_list(cookie)
    get_info(cookie)
