# coding=utf-8
__author__ = 'wb-zhangjinzhong'

import mySpiderBase

import mySpiderTools
import mySpiderTools2
import myDataTools
from pyquery import PyQuery as pq
import mySpiderCfg
from sqlobject import *
import myCommonToolsZ as tz

import threading
import datetime

import Queue
import time
import thread

import traceback

import json

acqHtml = mySpiderTools2.tryAcqHtml


class MySpiderT(mySpiderBase.MySpiderBase):
    rangeMain = range(1, 23 + 1)
    mainUrl = 'http://asktao.17173.com/wz/gl_%d.shtml'

    specialMainActionUrl = ('http://asktao.17173.com/wz/gl.shtml',)

    baseUrl = 'http://www.zjhz.lss.gov.cn'
    dbPath = 'D:/data/sqlite/askTao.db'
    tableName = 'askTaofaq'

    mainItemsSize = 50
    certainItemsSize = 50

    mainTCount = 1
    certainTCount = 2
    saveTCount = 2

    objMetaCfg = {
        'url': '',
        'title': '',
        'date': DateCol(),
        'author': '',
        'content': ''
    }

    def acqMainItemsAcqItems(self, page):
        return pq(page.decode('gb2312', 'ignore')).find('.art-list-txt li a')
        # return pq(page).find('.art-list-txt li a')

    def acqMainItemsPutToQ(self, item):

        peeps = self.wrapper.goalClass.selectBy(url=item.attr('href').strip())

        if peeps.count() != 0:
            return

        if item.attr('href') != '':
            self.mainItems.put(item.attr('href'))

    def acqCertainItemsSingle(self, itemMain, acqCount):

        try:
            page = acqHtml(itemMain).decode('gb2312', 'ignore')
            # page = acqHtml(itemMain)
        except:
            return False,

        q = pq(page)

        def getDate():
            t = datetime.datetime(1999, 9, 9).date()
            try:
                t = datetime.datetime.strptime(q.find('.col-01:eq(0)').text().strip()[3:],
                                               '%Y-%m-%d').date()
            except:
                pass
            return t

        # try:
        # objT = {'name': q.find('table.tsjb_nr tr:eq(0) td:eq(0)').text().strip(),
        #         'email': q.find('table.tsjb_nr tr:eq(0) td:eq(1)').text(),
        #         'title': q.find('table.tsjb_nr tr:eq(1) td:eq(0)').text(),
        #         'type': q.find('table.tsjb_nr tr:eq(1) td:eq(1)').text(),
        #         'content': q.find('table.tsjb_nr tr:eq(2) td:eq(0)').text(),
        #         'replyTime': getDate(),
        #         'replyContent': mySpiderTools.myDecodeHtml(q.find('table.tsjb_nr tr:eq(4) td:eq(0)').text().strip())
        #         }

        q.find('.content:eq(1) p:last').remove()

        objT = {
            'url': itemMain,
            'title': q.find('.article h1').text().strip(),
            'date': getDate(),
            'author': q.find('.info .col-02').text().strip(),
            'content': mySpiderTools.myDecodeHtml(q.find('.content:eq(1)').text().strip()),
        }
        # except :
        #     traceback.extract_stack()
        #     return False,

        if objT['title'] != '':

            peeps = self.wrapper.goalClass.selectBy(title=objT['title'])

            if peeps.count() != 0:
                return False,

            self.certainItems.put(objT)

        return True, objT

    def getItemInfo(self, item):
        return item['title']


if __name__ == '__main__':
    t = MySpiderT()
    # t.run()

    t.wrapper.exportTxt('D:/data/text/askTao', lambda (ele): ele.title, lambda (ele): tz.replaceCRLF(ele.content),
                        t.wrapper.goalClass.q.title.contains(u'钱'))

    # url = 'http://asktao.17173.com/content/2015-11-14/20151114185140358.shtml'
    #
    # page = acqHtml(url)
    #
    # print page
