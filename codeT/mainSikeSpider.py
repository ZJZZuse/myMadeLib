# coding=utf-8
__author__ = 'wb-zhangjinzhong'

import mySpiderBase2

import mySpiderTools
import mySpiderTools2
import myDataTools
from pyquery import PyQuery as pq
import mySpiderCfg2
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


class MySpiderT(mySpiderBase2.MySpiderBase):
    mySpiderCfgCfg = {

        'range': range(1, 99),

        'baseUrl': u'基础地址，通常用于页面省略地址补全',

        'specialMainActionUrl': (),

        # common is address
        'mainActionUrl': 'http://yuhongmeng.haodf.com/zixun/list.htm?type=&p=%d',
        # such as mainActionUrls = ({'url': '', 'range': range(1,3 + 1)},)
        'mainActionUrls': ()}

    dbPath = 'D:/data/sqlite/biyan.db'
    tableName = 'biyanyuhongmeng'

    mainItemsSize = 50
    certainItemsSize = 50

    mainTCount = 1
    certainTCount = 2
    saveTCount = 2

    objMetaCfg = {
        'url': '',
        'sickName': '',
        'title': '',

        'relSick': '',
        'dialogueCount': IntCol(),
        'lastPublishDate': DateTimeCol(),
        'content': ''
    }

    def acqMainItemsAcqItems(self, page):

        q = pq(page.decode('gb2312', 'ignore'))
        q.find('.zixun_list table tr:first').remove()

        return q.find('.zixun_list table tr')

    def acqMainItemsPutToQ(self, item):

        pq(item.find('td')[4]).find('font').remove()

        objT = {
            'url': pq(item.find('td')[3]).find('a').attr('href'),
            'sickName': pq(item.find('td')[1]).text().strip(),
            'title': pq(item.find('td')[2]).text().strip(),

            'relSick': pq(item.find('td')[3]).text().strip(),
            'dialogueCount': int(pq(item.find('td')[4]).text().strip()[0:-3]),
            'lastPublishDate': datetime.datetime.strptime(pq(item.find('td')[5]).find('span').text().strip(),
                                                          "%Y-%m-%d %H:%M:%S"),
            'content': ''
        }

        peeps = self.wrapper.goalClass.selectBy(url=objT['url'])

        if peeps.count() != 0:
            return

        if objT['url'] != '':
            self.mainItems.put(objT)

    def acqCertainItemsSingle(self, itemMain, acqCount):

        try:
            page = acqHtml(itemMain['url']).decode('gb2312', 'ignore')
        except:
            return False,

        q = pq(page)

        objT = itemMain.copy()

        objT['content'] = mySpiderTools.myDecodeHtml(q.find('.stream_left_content').html().strip())

        return True, objT

    def getItemInfo(self, item):
        return item['title']


if __name__ == '__main__':
    t = MySpiderT()
    t.run()

    # url = 'http://yuhongmeng.haodf.com/zixun/list.htm?type=&p=1'

    # url = 'http://www.haodf.com/wenda/yuhongmeng_g_3714898527.htm'
    #
    # page = acqHtml(url)
    #
    # print page
