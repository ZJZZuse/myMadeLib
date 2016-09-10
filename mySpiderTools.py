# encoding=utf-8
__author__ = 'Zhang'

import urllib
import sys
import socket
import myCommonToolsZ as zTools
import os
import html2text
import mySpiderCfg

'''
common use for other file
'''

# pq = mySpiderTools.pq
# acqHtml = mySpiderTools.tryGetHtml
# myDecodeHtml = mySpiderTools.myDecodeHtml

MySpiderCfg = mySpiderCfg.MySpiderCfg

h = html2text.HTML2Text()
h.ignore_links = True

timeout = 10  # in seconds


def setdefaulttimeout(timeout):
    socket.setdefaulttimeout(timeout)


setdefaulttimeout(timeout)


def myDecodeHtml(content):
    return h.handle(content.strip())


def downLoadResource(fileName, url, goalTime=3, passIfExist=True):
    '''
    @Deprecated
    @see thisModalName2
    :param
    fileName:
    :param
    url:
    :param
    goalTime:
    :param
    passIfExist:
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
    '''
    @Deprecated
    @see thisModalName2
    :param url:
    :param tryCount:
    :return:
    '''
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
    '''
    @Deprecated
    @see thisModalName2
    :param url:
    :return:
    '''
    # page = urllib.urlopen(url,proxies={'http':"http://222.79.72.120:8090"})
    page = urllib.urlopen(url)

    html = page.read()
    return html
