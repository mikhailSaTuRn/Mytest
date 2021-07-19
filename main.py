import threading

import urllib.request as urllib2
from bs4 import *
from urllib.parse  import urljoin

from pywebcopy import save_webpage

# Эту функцию я скачал из интернета
def crawl(pages, depth=None):
    indexed_url = []
    x = len(pagelist[0])
    for i in range(depth):
        for page in pages:
            if page not in indexed_url:
                indexed_url.append(page)
                try:
                    c = urllib2.urlopen(page)
                except:
                    print( "Could not open %s" % page)
                    continue
                soup = BeautifulSoup(c.read())
                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                                continue
                        url = url.split('#')[0]
                        if url[0:x] == pagelist[0]:
                            if url not in indexed_url:
                                indexed_url.append(url)
        pages = indexed_url
    return indexed_url

pagelist=["https://translate.google.com/"]
urls = crawl(pagelist, depth=1)
print(urls)
print(len(urls))


def fn(result):
    url = result
    length = len(url)
    d = 0
    for i in range(length-1, 0, -1):
        if url[i] == '/':
            d = i
            break
    page_name = url[d:]
    urllib2.urlretrieve(url, '/home/mikhail/1' + page_name)

def experiment():
    threads = []
    nThreads = 5
    count = 0
    for i in range(nThreads):
        result = urls[i]
        t = threading.Thread(target=fn, args=(result, ))
        t.start()
        threads.append([t, result])
        count += 1
        if count == 5 and count < (len(urls)-1):
            nThreads += 5
    thread_number = 1
    for thread, result in threads:
        thread.join()
        thread_number = thread_number + 1

if __name__ == "__main__":
    experiment()