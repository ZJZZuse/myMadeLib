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
    rangeMain = range(1, 231 + 1)
    mainUrl = 'http://wanwd.gyyx.cn/Article/ListForArticle?PageIndex=%d&PageSize=5&PrimaryCategoryId=21&CategoryId=0&Orderby=1'

    specialMainActionUrl = ()

    baseUrl = 'http://wanwd.gyyx.cn/article/'
    dbPath = 'D:/data/sqlite/askTaoOfficial.db'
    tableName = 'askTaoInfo'

    mainItemsSize = 50
    certainItemsSize = 50

    mainTCount = 1
    certainTCount = 2
    saveTCount = 2

    objMetaCfg = {
        'url': '',
        'parentTypeName': '',
        'typeName': '',
        'title': '',
        'author': '',
        'publishTime': DateTimeCol(),
        'viewCount': IntCol(),
        'content': ''
    }

    def acqMainItemsAcqItems(self, page):
        objT = json.loads(page)

        if not objT['Success']:
            return ()

        return objT['Data']['List']
        # return pq(page).find('.art-list-txt li a')

    def preDealWithItem(self,item):
        return item

    def acqMainItemsPutToQ(self, item):

        peeps = self.wrapper.goalClass.selectBy(title=item['Title'].strip())

        if peeps.count() != 0:
            return

        if item['Title'] != '':

            objT = {
                'url': self.baseUrl + str(item['Code']),
                'parentTypeName':item['ParentName'],
                'typeName': item['Name'],
                'title': item['Title'],
                'author': item['AuthorName'],
                'publishTime': datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int( item['CreateTime'][6:-5])) ), "%Y-%m-%d %H:%M:%S")  ,
                'viewCount': 0,
                'content': ''
            }

            self.mainItems.put(objT)

    def acqCertainItemsSingle(self, itemMain, acqCount):

        try:
            page = acqHtml(itemMain['url'])
            # page = acqHtml(itemMain)
        except:
            return False,

        q = pq(page)

        objT = itemMain.copy()

        objT['viewCount'] = int(q.find('.checknum strong').text())
        objT['content'] = mySpiderTools.myDecodeHtml(q.find('.share_info').html())

        if objT['title'] != '':

            peeps = self.wrapper.goalClass.selectBy(title=objT['title'])

            if peeps.count() != 0:
                return False,

            self.certainItems.put(objT)

            return True, objT

        else:
            return False,

    def getItemInfo(self, item):
        return item['title']


if __name__ == '__main__':
    t = MySpiderT()
    t.run()

    # t.wrapper.exportTxt('D:/data/text/askTao', lambda (ele): ele.title, lambda (ele): tz.replaceCRLF(ele.content),
    #                     t.wrapper.goalClass.q.title.contains(u'钱'))

    # url = 'http://wanwd.gyyx.cn/article/4696'
    #
    # page = acqHtml(url)
    #
    # print page
