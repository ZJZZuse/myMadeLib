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
    rangeMain = range(1, 2 + 1)
    mainUrl = 'http://www.zjhz.lss.gov.cn/html/jlhd/ckhf.html?qry_useridcard=&qry_username=&_currpage=%d&_pagelines=20&_rowcount=4646'
    baseUrl = 'http://www.zjhz.lss.gov.cn'
    dbPath = 'D:/abc/download/shebao.db'
    tableName = 'sheBaoFAQ'

    mainItemsSize = 50
    certainItemsSize = 50

    mainTCount = 1
    certainTCount = 2
    saveTCount = 2

    objMetaCfg = {'name': '',
                  'email': '',
                  'title': '',
                  'type': '',
                  'content': '',
                  'replyTime': DateTimeCol(),
                  'replyContent': ''
                  }

    def acqMainItemsAcqItems(self, page):
        return pq(page.decode('gb2312','ignore')).find('table.tsjb_nr tr a')

    def acqMainItemsPutToQ(self, item):

        peeps = self.wrapper.goalClass.selectBy(name=item.text().strip())

        if peeps.count() != 0:
            return

        if item.attr('href') != '':
            self.mainItems.put(self.baseUrl + item.attr('href'))

    def acqCertainItemsSingle(self, itemMain, acqCount):

        try:
            page = acqHtml(itemMain).decode('gb2312','ignore')
        except:
            return False,

        q = pq(page)

        def getDate():
            t = datetime.datetime(1999, 9, 9)
            try:
                t = datetime.datetime.strptime(q.find('table.tsjb_nr tr:eq(3) td:eq(0)').text().strip(),
                                               '%Y-%m-%d %H:%M:%S')
            except:
                pass
            return t

        # try:
        objT = {'name': q.find('table.tsjb_nr tr:eq(0) td:eq(0)').text().strip(),
                'email': q.find('table.tsjb_nr tr:eq(0) td:eq(1)').text(),
                'title': q.find('table.tsjb_nr tr:eq(1) td:eq(0)').text(),
                'type': q.find('table.tsjb_nr tr:eq(1) td:eq(1)').text(),
                'content': q.find('table.tsjb_nr tr:eq(2) td:eq(0)').text(),
                'replyTime': getDate(),
                'replyContent': mySpiderTools.myDecodeHtml(q.find('table.tsjb_nr tr:eq(4) td:eq(0)').text().strip())
                }
        # except :
        #     traceback.extract_stack()
        #     return False,

        if objT['name'] != '':

            peeps = self.wrapper.goalClass.selectBy(name=objT['name'])

            if peeps.count() != 0:
                return False,

            self.certainItems.put(objT)

        return True, objT

    def getItemInfo(self, item):
        return item['title']


if __name__ == '__main__':
    t = MySpiderT()
    t.run()

    # url = 'http://www.zjhz.lss.gov.cn/html/jlhd/ckhf_nr.html?seq_id=2015111200145455943981'
    #
    # page = acqHtml(url)
    #
    # print page
