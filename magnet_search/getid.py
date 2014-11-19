import os, sys, hashlib
import pickle
import re


if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen


BASE_URL = 'http://www.javzoo.com/en/released/currentPage/{}'
VIDEO_ID_MATCH = r'(?P<ID>[A-Z]+\-[0-9]+)'

id_pool = set()
hash_pool = set()


def extract_id(buff):
    global id_pool

    if type(buff) == bytes:
        buff = buff.decode()

    ids = re.findall(VIDEO_ID_MATCH, buff)
    for id in ids:
        id_pool.add(id)
    return len(ids)

def read_page():
    global id_pool

    page_num = 1 
    while True:
        full_url = BASE_URL.format(page_num)
        buff = urlopen(full_url).read()
        hash_result = hashlib.md5(buff).hexdigest()
        if hash_result in hash_pool:
            print('All page has been cached'.format(page_num))
            break
        print('Page {} is cached'.format(page_num))
        extract_id(buff)
        hash_pool.add(hash_result)
        pickle.dump(id_pool, id_fp)
        page_num += 1


if __name__ == "__main__":

    id_filename = 'id.bin'
    if os.path.isfile(id_filename):
        # read
        id_fp = open(id_filename, 'rb')
        id_pool = pickle.load(id_fp)
        id_fp.close()
        print(id_pool)


    # write
    id_fp = open(id_filename, 'wb')

    
    read_page()


    pickle.dump(id_pool, id_fp)
    id_fp.close()
