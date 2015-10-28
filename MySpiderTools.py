# encoding=utf-8
__author__ = 'Zhang'

import urllib
import sys
import socket, ftplib
from pyquery import PyQuery as pq
from myMadeLib import MyCommonToolsZ

zTools = MyCommonToolsZ.MyCommonToolsZ

class MySpiderTools:
    '''
    MySpiderTools
    '''
    timeout = 10  # in seconds

    @classmethod
    def setdefaulttimeout(cls):
        socket.setdefaulttimeout(cls.timeout)

    @staticmethod
    def downLoadResource(fileName, url, goalTime = 3):
        tryTime = 0
        while True:
            print 'start downLoad'

            if (tryTime >= goalTime):
                print 'had tried %d time(s),but failed!' % goalTime
                return

            if (tryTime > 0):
                print 'had tried %d time(s) for' % tryTime, fileName

            try:
                urllib.urlretrieve(url, fileName)
                print 'had downloaded %s' % fileName
                break
            except Exception, e:
                # urllib.urlretrieve(urlT,fileName.decode('utf-8'))
                try:
                    os.remove(fileName)
                except Exception, e:
                    zTools.commonErrorPrint(e)

                zTools.commonErrorPrint(e)
            finally:
                tryTime += 1
    @classmethod
    def getHtml(cls,url, tryCount=3):
        i = 0

        while i < tryCount:

            c = cls.getHtmlI(url)

            if c != '':
                return c
            else:
                i += 1

        return ''

    @classmethod
    def getHtmlI(cls,url):
        try:
            page = urllib.urlopen(url)
            html = page.read()
            return html
        except Exception, e:
            print e.__class__, e
            return ''


MySpiderTools.setdefaulttimeout()