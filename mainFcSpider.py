# coding=utf-8
__author__ = 'wb-zhangjinzhong'

import mySpiderTools
import mySpiderTools2
import myDataTools
import pyquery.pyquery
import mySpiderCfg
from sqlobject import *
import myCommonToolsZ as tz

import threading

import Queue

def startThread(fn):
    threading

acqHtml = mySpiderTools2.tryAcqHtml
pq = pyquery.pyquery

gameMetaCfg = {
    'name': '',
    'softwareVersion': '',
    'ename': '',
    'img': BLOBCol(),
    'gameType': '',
    'inLanguage': '',
    'fileSize': '',
    'fileComany': '',
    'startingTime': '',
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

    global mainItems,gameItems,mySpiderCfgMain,wrapper

    wrapper = myDataTools.DataWrapper('fgGamesFromYouxun', myDataTools.DataWrapper(gameMetaCfg))

    mainItems = Queue.Queue(50)
    gameItems = Queue.Queue()

    mySpiderCfgMain = mySpiderCfg.MySpiderCfg('http://www.yxdown.com','http://www.yxdown.com/zj/Catalog_182_softTime_%d.html',range(1,42))


def main():
    '''
    2 queues
    :return:
    '''

    threading.Thread(target=acqMainItems)

    time.sleep(1)


    tz.fireActionTimes(lambda : threading.Thread(target=dealCertainItem),2)

    time.sleep(1)

    tz.fireActionTimes(lambda : threading.Thread(target=storeGames),3)

def acqMainItems():

    page = acqHtml(mySpiderCfgMain.iter.next())

    items = pq(tz.decodeForThisSys(page)).find('.nr3 dd a')

    for item in items:
        itemT = pq(item)



    pass


def dealCertainItem():
    pass


def storeGames():
    pass


if __name__ == '__main__':

    url = 'http://www.yxdown.com/SoftView/SoftView_29498.html'

    # page = acqHtml('http://www.yxdown.com/zj/Catalog_182_softTime_1.html#new_games')

    page = acqHtml(url)

    print tz.decodeForThisSys(page)
