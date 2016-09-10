# coding=utf-8

# RANGE_MAIN = range(1, 7)
# MAIN_URL = 'http://www.yxdown.com/zj/Catalog_199_softTime_%d.html'
# DB_PATH = 'D:/abc/download/games.db'
# TABLENAME = 'MDGamesFromYouxun'

RANGE_MAIN = range(1, 23 + 1)
MAIN_URL = 'http://www.jb51.net/books/list152_%d.html'
DB_PATH = 'D:/abc/download/javaBook.db'
TABLENAME = 'javaBook'

__author__ = 'wb-zhangjinzhong'

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

import json

'''
0.1beta,基本能正常运行，还有游戏类型，线程自动终止的问题。适合于解析游讯网，能解析大部分游戏
'''

acqHtml = mySpiderTools2.tryAcqHtml

gameMetaCfg = {
    'name': '',
    'fileSize': '',
    'note':'',
    'url': '',
    'updateDate' : ''
}


def initDate():
    myDataTools.DataWrapper.initDb(DB_PATH)

    global mainItems, gameItems, mySpiderCfgMain, wrapper

    wrapper = myDataTools.DataWrapper(TABLENAME, myDataTools.DataWrapper.wrappeByCommonFieldCfg(gameMetaCfg))

    mainItems = Queue.Queue(500)
    gameItems = Queue.Queue(500)

    mySpiderCfgMain = mySpiderCfg.MySpiderCfg('http://www.jb51.net',
                                              MAIN_URL, RANGE_MAIN)

    mySpiderCfgMain.countT = 0
    mySpiderCfgMain.addCount = 0


def main():
    '''
    2 queues
    :return:
    '''

    initDate()

    threading.Thread(target=acqMainItems).start()

    time.sleep(1)

    tz.fireActionTimes(lambda: threading.Thread(target=dealCertainItem).start(), 2)

    time.sleep(1)

    tz.fireActionTimes(lambda: threading.Thread(target=storeGames).start(), 3)


def acqMainItems():
    while True:

        try:
            page = acqHtml(mySpiderCfgMain.iter.next()).decode('gb2312', 'ignore')

        except:
            print 'done'
            return

        items = pq(page).find('ul.cur-cat-list dt.clearfix a')

        for item in items:
            itemT = pq(item)

            peeps = wrapper.goalClass.selectBy(url=itemT.attr('href'))

            if peeps.count() == 0:
                mainItems.put(mySpiderCfgMain.baseUrl + itemT.attr('href'))


def dealCertainItem():
    while True:

        # if mainItems.empty():
        #     time.sleep(5)
        #     if mainItems.empty():
        #         return

        urlT = mainItems.get()

        page = acqHtml(urlT).decode('gb2312', 'ignore')

        q = pq(page)


        gameObj = {
            'name': q.find('h1[itemprop=name]').text(),
            'fileSize': q.find('#param-content span[itemprop=fileSize]').text(),
            'note': q.find('#soft-intro').text().strip(),
            'url': urlT,
            'updateDate': q.find('#param-content span[itemprop=dateModified]').text()
        }

        if len(gameObj['name']) != 0:
            gameItems.put(gameObj)
            print 'now index is %d,put %s' % (mySpiderCfgMain.countT, gameObj['name'])

            # lockT = thread.allocate_lock()

            # lockT.acquire()
            mySpiderCfgMain.countT += 1
            # lockT.release()


def storeGames():
    while True:
        # if gameItems.empty():
        #     time.sleep(5)
        #     if gameItems.empty():
        #         return

        item = gameItems.get()

        try:
            wrapper.add(item)
        except:
            print 'wrapper.add(item) wrong at %s' % item

        print 'index is %d,added %s' % (mySpiderCfgMain.addCount, item['name'])

        mySpiderCfgMain.addCount += 1
    pass


if __name__ == '__main__':
    # url = 'http://www.yxdown.com/SoftView/SoftView_29498.html'
    #
    # # page = acqHtml('http://www.yxdown.com/zj/Catalog_182_softTime_1.html#new_games')
    #
    # page = acqHtml(url)
    #
    # print tz.decodeForThisSys(page)

    main()

    # def a ():
    #     c = 1
    #     def b():
    #         print c
    #
    #     b()
    #
    # a()
