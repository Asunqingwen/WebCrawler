'''
搜狐体育——NBA新闻标题和链接爬虫
'''
import re
from collections import deque
from urllib.parse import urljoin
import requests
import builtwith
import whois

A_LI_PATTERN = re.compile(r'<li class="item">.*?</li>')
A_TEXT_PATTERN = re.compile(r'<a\s+[^>]*?>(.*?)</a>')
A_HREF_PATTERN = re.compile(r'<a\s+[^>]*?href="(.*?)"\s*[^>]*?>')


def decode_page(page_bytes, charsets):
    '''
    通过指定的字符集对页面进行解码
    :param page_bytes:页面内容
    :param charsets: 字符集
    :return:
    '''
    for charset in charsets:
        try:
            return page_bytes.decode(charset)
        except UnicodeDecodeError:
            pass


def get_matched_parts(content_string, pattern):
    '''
    从字符串中提取正则表达式匹配的内容
    :param content_string: 字符串
    :param pattern: 正则式
    :return:
    '''
    return pattern.findall(content_string, re.I) if content_string else []


def get_matched_part(content_string, pattern, group_no=1):
    '''
    从字符串中提取正则表达式匹配的内容
    :param content_string: 字符串
    :param pattern: 正则式
    :param group_no: 组号
    :return:
    '''
    match = pattern.search(content_string)
    if match:
        return match.group(group_no)


def get_page_html(seed_url, *, charsets=('utf-8',)):
    '''
    获取页面的HTML代码
    :param seed_url:起始页
    :param charsets: 字符集
    :return:
    '''
    resp = requests.get(seed_url)
    if resp.status_code == 200:
        return decode_page(resp.content, charsets)


def repair_incorrect_href(current_url, href):
    '''
    修正获取的href属性
    :param current_url: 当前页面
    :param href: 获取的href
    :return:
    '''
    if href.startswith('//'):
        href = urljoin('https://', href)
    elif href.startswith('/'):
        href = urljoin(current_url, href)
    return href if href.startswith('http') else ''


def start_crawl(seed_url, pattern, *, max_depth=-1):
    '''
    开始爬虫
    :param seed_url: 开始网页
    :param pattern: 正则匹配
    :param max_depth: 层数
    :return:
    '''
    new_urls, visited_urls = deque(), set()
    new_urls.append((seed_url, 0))
    while new_urls:
        current_url, depth = new_urls.popleft()
        if depth != max_depth:
            page_html = get_page_html(current_url, charsets=('utf-8', 'gbk'))
            contents = get_matched_parts(page_html, pattern)
            for content in contents:
                text = get_matched_part(content, A_TEXT_PATTERN)
                href = get_matched_part(content, A_HREF_PATTERN)
                if href:
                    href = repair_incorrect_href(current_url, href)
                print(text, href)
                if href and href not in visited_urls:
                    new_urls.append((href, depth + 1))


if __name__ == '__main__':
    # print(builtwith.parse("https://sports.sohu.com"))
    # print(whois.whois("https://sports.sohu.com/"))
    start_crawl(
        seed_url='https://sports.sohu.com/s/nba',
        pattern=A_LI_PATTERN,
        max_depth=2
    )
