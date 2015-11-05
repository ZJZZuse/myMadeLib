# coding=utf-8
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
    'pf_score_des': '',
    'game_des': '',
    'gameUrl': ''
}



def initDate():
    myDataTools.DataWrapper.initDb('games.db')

    global mainItems, gameItems, mySpiderCfgMain, wrapper, countT



    countT = int(0)

    wrapper = myDataTools.DataWrapper('fgGamesFromYouxun', myDataTools.DataWrapper.wrappeByCommonFieldCfg(gameMetaCfg))

    mainItems = Queue.Queue(500)
    gameItems = Queue.Queue(500)

    mySpiderCfgMain = mySpiderCfg.MySpiderCfg('http://www.yxdown.com',
                                              'http://www.yxdown.com/zj/Catalog_182_softTime_%d.html', range(1, 42))

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
            page = tz.decodeForThisSys(acqHtml(mySpiderCfgMain.iter.next()))

        except:
            print 'done'
            return

        items = pq(tz.decodeForThisSys(page)).find('.nr3 dd a')

        for item in items:
            itemT = pq(item)

            peeps = wrapper.goalClass.selectBy(gameUrl=itemT.attr('href'))

            if peeps.count() == 0:
                mainItems.put(itemT.attr('href'))


def dealCertainItem():
    while True:

        # if mainItems.empty():
        #     time.sleep(5)
        #     if mainItems.empty():
        #         return

        urlT = mainItems.get()

        page = tz.decodeForThisSys(acqHtml(urlT))

        q = pq(page)

        def acqScore():
            id = q.find('#softid').val()

            if id == None:
                return -1.0

            try:
                objT = json.loads(
                    acqHtml('http://dy.www.yxdown.com/open/op.ashx?action=/soft/votes/data.json&sid=%s' % id))
            except:
                print 'http://dy.www.yxdown.com/open/op.ashx?action=/soft/votes/data.json&sid=%s' % id
                return -1.0

            r = objT['Score']

            return r

        def acqImg():
            r = ''
            url = q.find('div.dl>dl>dd>img').attr('src')

            if not tz.emptyOrNoneAll(url):
                r = acqHtml(url)

            return r

        def acqDate(str):
            r = datetime.date(1949, 10, 1)

            if not tz.emptyOrNoneAll(str):
                try:
                    r = datetime.datetime.strptime(str, '%Y/%m/%d').date()
                except:
                    return r

            return r

        if q.find('h1[itemprop=name]').text().strip() == '':
            continue

        gameObj = {
            'name': q.find('h1[itemprop=name]').text().strip(),
            'softwareVersion': 'fc',
            'ename': q.find('span.ename').text().strip(),
            'img': acqImg(),
            'gameType': q.find('div.dl>dl>dt>span:eq(0)>b:eq(0)>a').text(),
            'inLanguage': q.find('div.dl>dl>dt>span:eq(0)>b:eq(1)>em').text(),
            'fileSize': q.find('div.dl>dl>dt>span:eq(1)>b:eq(0)>em').text(),
            'fileComany': q.find('div.dl>dl>dt>span:eq(1)>b:eq(1)>em').text(),
            'startingTime': acqDate(q.find('div.dl>dl>dt>span:eq(2)>b:eq(0)>em').text()),
            'dateModified': acqDate(q.find('div.dl>dl>dt>span:eq(2)>b:eq(1)>em').text()),
            'operatingSystem': q.find('div.dl>dl>dt>span:eq(3) a').text(),
            'tag': q.find('div.dl>dl>dt>span:eq(4)>em').text(),
            'zt_text': q.find('div.dl>dl>dt>span:eq(5)>em').text(),
            'pf_score': acqScore(),
            'pf_score_des': q.find('div.pinja_box').text().strip(),
            'game_des': mySpiderTools.myDecodeHtml(q.find('li.yx1>span').text().strip()),
            'gameUrl': urlT
        }

        if len(gameObj['name']) != 0:
            gameItems.put(gameObj)
            print 'now index is %d,put %s' %(mySpiderCfgMain.countT ,gameObj['name'])

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

        wrapper.add(item)

        print 'index is %d,added %s' % (mySpiderCfgMain.addCount,item['name'])

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

