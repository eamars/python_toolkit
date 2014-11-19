from bs4 import BeautifulSoup
import sys
import re
from tools import load_video_id, date_to_int, size_to_int

if sys.version_info < (3, 0):
    from urllib2 import urlopen
    from urllib2 import quote
else:
    from urllib.request import urlopen
    from urllib.parse import quote

SEARCH_URL = 'http://www.btspread.com/search/{}'
MAGNET = 'magnet:?xt=urn:btih:{}&dn={}'
HASH_REGEX = r'[0-9A-Z]+'

def selector(dl_list):
    best_rank = 0
    best = dl_list[0]
    for dl_obj in dl_list:
        date = dl_obj['date']
        size = dl_obj['size']
        rank = date_to_int(date) + size_to_int(size)
        if rank > best_rank:
            best_rank = rank
            best = dl_obj
    return best

def get_dl_obj(id):

    try:
        html = urlopen(SEARCH_URL.format(id))
    except Exception as e:
        print(e)
        return None
    
    parsed_html = BeautifulSoup(html)

    tbody = parsed_html.find('tbody')
    if not tbody:
        return None
    tr = tbody.find_all('tr')

    dl_list = []
    for element in tr:
        dl_obj = dict()


        dl_obj['title'] = element.find('a', attrs={'class': 'btn'})['title']
        dl_obj['url'] = element.find('a', attrs={'class': 'btn'})['href']
        dl_obj['hash'] = re.findall(HASH_REGEX, dl_obj['url'])[0]
        dl_obj['size'] = element.find('td', attrs={'class': 'files-size'}).contents[0]
        dl_obj['date'] = element.find('td', attrs={'class': 'convert-date'}).contents[0]
        dl_obj['magnet_url'] = MAGNET.format(dl_obj['hash'], quote(dl_obj['title']))

        dl_list.append(dl_obj)

    return dl_list

if __name__ == "__main__":

    for id in load_video_id('id.bin')[1]:
        dl_obj = get_dl_obj(id)
        if dl_obj:
            print(id, end=': ')
            print(selector(dl_obj)['magnet_url'])