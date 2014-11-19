import pickle
from datetime import date
from math import log as log

def load_video_id(fname):
    fp = open(fname, 'rb')

    id_pool = pickle.load(fp)

    return (len(id_pool), id_pool)

def date_to_int(date_str):
    spl = date_str.split('-')
    dt = date(int(spl[0]), int(spl[1]), int(spl[2]))
    return log(dt.toordinal() / date.today().toordinal()) * 1000

def size_to_int(size_str):
    size = float(size_str[:-2])
    unit = size_str[-2:]
    factor = 0
    if unit == "GB":
        factor = 1024
    elif unit == "MB":
        factor = 1
    elif unit == "KB":
        factor = 1/1024
    elif unit == "TB":
        factor = 1024 * 1024

    return log(1024 / (size * factor)) / 10

if __name__ == "__main__":
    print(date_to_int("2014-8-15"))