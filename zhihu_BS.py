'''获取知乎发现上的问题链接'''
import re
from urllib.parse import urljoin
import bs4
import requests

headers = {'user-agent': 'Baiduspider'}
base_url = 'https://www.zhihu.com/'
resp = requests.get(urljoin(base_url, 'explore'), headers=headers)
soup = bs4.BeautifulSoup(resp.text, 'lxml')
href_regex = re.compile(r'^/question|/answer')
links_set = set()
for a_tag in soup.find_all('a', {'href': href_regex}):
    if 'href' in a_tag.attrs:
        href = a_tag.attrs['href']
        full_url = urljoin(base_url, href)
        links_set.add((full_url, a_tag.text))
print('Total %d question pages found.' % len(links_set))
print(links_set)
