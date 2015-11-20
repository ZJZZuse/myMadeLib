# coding=utf-8
__author__ = 'wb-zhangjinzhong'

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


class MySpiderBase:
    '''
    基础自定义爬虫类，简单的爬虫继承该类即可，覆写acqMainItemsAcqItems，acqMainItemsPutToQ，acqCertainItemsSingle
    '''

    mySpiderCfgCfg = {

        'baseUrl': u'基础地址，通常用于页面省略地址补全',

        'specialMainActionUrl': (),

        #common is address
        'mainActionUrl': False,
        # such as mainActionUrls = ({'url': '', 'range': range(1,3 + 1)},)
        'mainActionUrls': ()

    }

    dbPath = 'D:/abc/download/games.db'
    tableName = 'fcChineseGamesFromYouxun'

    mainItemsSize = 50
    certainItemsSize = 50

    mainTCount = 1
    certainTCount = 2
    saveTCount = 2

    objMetaCfg = {'name': '',
                  'softwareVersion': '',
                  'ename': '',
                  'img': BLOBCol(),
                  'gameType': '',
                  'inLanguage': '',
                  'fileSize': '',
                  'fileComany': '',
                  'startingTime': DateCol(),
                  'dateModified': DateCol(),
                  'operatingSystem': '',
                  'tag': '',
                  'zt_text': '',
                  'pf_score': FloatCol(),
                  'commentCount': IntCol(),
                  'pf_score_des': '',
                  'game_des': '',
                  'gameUrl': '',
                  'commentAll': ''}

    mainItems = None
    certainItems = None

    mainIsDone = False
    acqCertainItemsIsDone = False

    def __init__(self):
        self.initDate()

    def initDate(self):
        myDataTools.DataWrapper.initDb(self.dbPath)

        self.wrapper = myDataTools.DataWrapper(self.tableName,
                                               myDataTools.DataWrapper.wrappeByCommonFieldCfg(self.objMetaCfg))

        self.mainItems = Queue.Queue(self.mainItemsSize)
        self.certainItems = Queue.Queue(self.certainItemsSize)
        self.mySpiderCfgMain = mySpiderCfg2.MySpiderCfg(self.mySpiderCfgCfg)

        self.mySpiderCfgMain.savedCount = 0
        self.mySpiderCfgMain.acqCount = 0

    def run(self):
        '''
        main m

        :param mainTCount:
        :param certainTCount:
        :param saveTCount:
        :return:
        '''

        tz.fireActionTimes(lambda: threading.Thread(target=self.acqMainItems).start(), self.mainTCount)

        time.sleep(1)

        tz.fireActionTimes(lambda: threading.Thread(target=self.acqCertainItems).start(), self.certainTCount)

        time.sleep(1)

        tz.fireActionTimes(lambda: threading.Thread(target=self.saveCertainItems).start(), self.saveTCount)

    def acqMainItems(self):

        while True:
            try:
                page = self.acqMainPage()

            except StopIteration, e:
                self.mainIsDone = True
                print 'acqMainItems done in %s' % threading.currentThread().name
                return

            items = self.acqMainItemsAcqItems(page)

            for item in items:
                itemT = self.preDealWithItem(item)
                self.acqMainItemsPutToQ(itemT)

    def acqMainPage(self):
        return acqHtml(self.mySpiderCfgMain.iter.next())

    def preDealWithItem(self, item):
        return pq(item)

    def acqMainItemsAcqItems(self, page):
        '''

        :return:exa:pq(tz.decodeForThisSys(page)).find('.nr3 dd a')
        '''

        return None

    def acqMainItemsPutToQ(self, itemT):
        '''
        peeps = wrapper.goalClass.selectBy(gameUrl=itemT.attr('href'))

            if peeps.count() == 0:
                mainItems.put(itemT.attr('href'))
        :return:
        '''

        pass

    def acqCertainItems(self):
        while True:

            if self.mainIsDone and self.mainItems.empty():
                self.acqCertainItemsIsDone = True
                print 'acqCertainItems done in %s' % threading.currentThread().name

                return

            try:
                item = self.mainItems.get(timeout=10)
            except:
                continue

            rt = self.acqCertainItemsSingle(item, self.mySpiderCfgMain.acqCount)

            if rt[0]:
                self.mySpiderCfgMain.acqCount += 1
                print 'acqCount:%d,%s' % (self.mySpiderCfgMain.acqCount, self.getItemInfo(rt[1]))

    def getItemInfo(self, item):
        return item

    def acqCertainItemsSingle(self, itemMain, acqCount):
        '''

        page = tz.decodeForThisSys(acqHtml(urlT))
        q = pq(page)


        :return:
        '''

        return True

    def saveCertainItems(self):

        while True:

            if self.acqCertainItemsIsDone and self.certainItems.empty():
                self.wrapper.commit()

                print 'saveCertainItems done in %s' % threading.currentThread().name

                return

            try:
                item = self.certainItems.get(timeout=10)
            except:
                continue

            try:
                self.wrapper.add(item)
            except:
                traceback.print_exc()

            self.mySpiderCfgMain.savedCount += 1

            print 'savCount:%d,%s' % (self.mySpiderCfgMain.savedCount, self.getItemInfo(item))
