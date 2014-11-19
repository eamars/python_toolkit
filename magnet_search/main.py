from getmagnet import get_dl_obj, selector

dl_list = get_dl_obj('ABP-166')

if dl_list:
    selected = selector(dl_list)
    print("Title:", selected["title"])
    print("Size:", selected["size"])
    print("Date:", selected["date"])
    print("Magnet:", selected["magnet_url"])
else:
    print("Unable to find")