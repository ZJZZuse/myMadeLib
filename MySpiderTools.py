# encoding=utf-8
__author__ = 'Zhang'

import urllib
import sys
import socket, ftplib
from pyquery import PyQuery as pq
import myCommonToolsZ as zTools
import html2text
import os

'''
common use for other file
'''
# pq = mySpiderTools.pq
# acqHtml = mySpiderTools.tryGetHtml
# myDecodeHtml = mySpiderTools.myDecodeHtml


h = html2text.HTML2Text()
h.ignore_links = True

timeout = 10  # in seconds


class MySpiderCfg:
    baseUrl = 'http://yhyz.6000y.com'
    mainActionUrl = 'http://yhyz.6000y.com/news/news_140_%d.html'
    baseFilePath = 'F:/more/illusion/other/ling/other/text/aisirenText2/%s.txt'

    def __init__(self, baseUrl, mainActionUrl, baseFilePath):
        '''

        :param baseUrl:
        :param mainActionUrl:
        :param baseFilePath:
        :return:
        '''
        self.baseUrl = baseUrl
        self.mainActionUrl = mainActionUrl
        self.baseFilePath = baseFilePath


def setdefaulttimeout(timeout):
    socket.setdefaulttimeout(timeout)


setdefaulttimeout(timeout)


def myDecodeHtml(content):
    return h.handle(content.strip())


def downLoadResource(fileName, url, goalTime=3, passIfExist=True):
    '''

    :param fileName:
    :param url:
    :param goalTime:
    :param passIfExist:
    :return:
    '''
    if os.path.exists(fileName):
        return False

    for i in range(0, goalTime):

        if (i > 0):
            print 'now index is %d for %s' % (i, fileName)

        try:
            urllib.urlretrieve(url, fileName)
            print 'downloaded %s' % fileName
            return True
        except Exception, e:
            # urllib.urlretrieve(urlT,fileName.decode('utf-8'))
            try:
                os.remove(fileName)
            except Exception, e:
                zTools.commonErrorPrint(e)

            zTools.commonErrorPrint(e)

        if (i == goalTime - 1):
            print 'now index is %d for %s,but failed' % (i, fileName)

    return False


def tryGetHtml(url, tryCount=3):
    for i in range(0, tryCount):

        if i > 0:
            print '%s,now index is %s' % (sys._getframe().f_back.f_code.co_name, i)

        try:
            c = getHtml(url)
            return c
        except Exception, e:
            zTools.commonErrorPrint(e)


tryAcqHtml = tryGetHtml


def getHtml(url):
    # page = urllib.urlopen(url,proxies={'http':"http://222.79.72.120:8090"})
    page = urllib.urlopen(url)

    html = page.read()
    return html
