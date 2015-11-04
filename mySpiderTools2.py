# coding=utf-8
__author__ = 'wb-zhangjinzhong'

import urllib
import urllib2

import tryActionMEthodDecorator

import os

defaultHeadersCfg = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
    # ,
    # 'Referer':'https://www.baidu.com/'
}


@tryActionMEthodDecorator.tryActionMEthod(3)
def tryAcqHtml(url, data=None, headers=None, timeout=None):
    '''
    :param url:
    :param data:{'Referer':'https://www.baidu.com/'}
    :param headers:
    :return:
    '''

    return acqHtml(url, data=None, headers=None, timeout=None)

def acqHtml(url, data=None, headers=None, timeout=None):
    '''

    :param url:
    :param data:{'Referer':'https://www.baidu.com/'}
    :param headers:
    :return:
    '''
    headersT = defaultHeadersCfg.copy()

    if headers != None:
        headersT.update(headers)

    if data != None:
        data = urllib.urlencode(data)

    request = urllib2.Request(url, data, headersT)

    response = urllib2.urlopen(request, timeout=10)
    page = response.read()

    return page


def setProxy(proxy={}):
    '''

    :param proxy: such as {"http" : 'http://some-proxy.com:8080'}
    :return:
    '''

    proxy_handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

@tryActionMEthodDecorator.tryActionMEthod(3)
def tryDownloadResource(url,path,passIfExist = True):

    if passIfExist and os.path.exists(path):
        print 'file (%s) exists and pass by your commond' % path
        return False

    urllib.urlretrieve(url, path)
    print 'downloaded %s' % path

    return True



if __name__ == '__main__':
    # tryAction(lambda :1/0,5)

    url = 'http://www.baidu.com'

    # a = tryAcqHtml('http://www.baidu.com/home/msg/data/personalcontent?callback=jQuery110203679979813750833_1446444484594&num=8&_req_seqid=f768e33c00001cf9&sid=1432_17758_17619_12657_12824_17783_14432_17001_17072_15104_11452_17158_17051&_=1446444484596')
    #

    tryDownloadResource(url,'D:/abc/download/')

    # print a

