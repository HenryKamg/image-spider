#coding:utf8
import os, sys
import md5
import time, random
import requests
import urllib, urllib2
from termcolor import colored
import multiprocessing
from bs4 import BeautifulSoup

def for_one_page_test( url ):

    #opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'218.244.149.184:8888'}), urllib2.HTTPHandler(debuglevel=1))
    #urllib2.install_opener(opener)

    #opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'80.242.171.35:8888'}), urllib2.HTTPHandler(debuglevel=1))
    #urllib2.install_opener(opener)

    UA = "Mozilla/"+ str(random.randint(10, 100))  +".0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090625 Firefox/3.5"
    print UA

    i_headers = {"User-Agent": "Mozilla/8.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Referer": 'http://jiandan.net'}
    req = urllib2.Request(url, headers=i_headers)
    html = urllib2.urlopen(req).read()
    print colored( html , 'blue')
    soup = BeautifulSoup(html)

    for img_address in soup.find_all('a'):
        if ( isinstance(img_address.get('class'), (list,str) ) and img_address.get('class')[0] == "scrollLoading" ):
            try:            
                img_url = img_address.get('href')
                print colored( img_url[2:] , 'green')
                image_downlode( img_url )

            except Exception as e:  
                print Exception, ":", e

def image_downlode( url ):
    img = requests.get( 'http://' + url[2:] )
    name = get_name(url) + '.' + url[-3:] 
    try:
        open('/home/wwwroot/romance.wangxiaoting.cn/image/'+name,'wb').write(img._content)
        print ( name + " done!")
    except Exception as e:
        print Exception, ":", e
        print ( name + " flased!")
    pass

def get_name( url ):
    m = md5.new()
    m.update( url )
    return m.hexdigest()

if __name__ == "__main__":
    start = 5460
    end = 5480    
    pool = multiprocessing.Pool(processes = 5)

    btime = time.time()

    for page in range(start,end+1):
        url = "http://www.meizitu.com/a/" + str(page)
        pool.apply_async(for_one_page_test, (url, ) )

    pool.close()
    pool.join()

    etime = time.time()

    print (etime - btime)
