# coding=utf-8
__author__ = 'wb-zhangjinzhong'

from sqlobject import *
from new import classobj

import myCommonToolsZ as tz
import os

import traceback

# class tc(SQLObject):
#     pass
#
#
# t = tc.selectBy()
#
# t.count()

class DataWrapper:
    '''
    数据库包裹，暂时只支持sqlite，
    '''
    commonFieldCfg = {
        # 'name': StringCol(),
        'info_createTime': DateTimeCol()
    }

    goalClass = None

    @classmethod
    def wrappeByCommonFieldCfg(cls, p):
        '''
        添加常用配置，不覆盖客户同名配置
        :param p:
        :return:
        '''

        pt = cls.commonFieldCfg.copy()
        # 覆盖客户值
        pt.update(p)

        return pt

    @classmethod
    def initDb(cls, sqlitePath):
        '''
        初始化数据库连接，在应用里调用一次
        :param sqlitePath:
        :return:
        '''
        db_filename = os.path.abspath(sqlitePath)

        connection_string = 'sqlite:' + db_filename
        connection = connectionForURI(connection_string)

        connection.dbEncoding = 'utf-8'

        connection.autoCommit = False

        sqlhub.processConnection = connection

        cls.connection = connection

    @staticmethod
    def initFields(fields):
        '''

        :param fields: 空字符串默认变成 StringCol()
        :return:
        '''
        for key in iter(fields):
            if isinstance(fields[key], str) and len(fields[key]) == 0:
                fields[key] = StringCol()

    def __init__(self, tableName, fields):

        self.__class__.initFields(fields)

        self.goalClass = classobj(tableName, (SQLObject,), fields)

        # self.goalClass._connection.debug = True

        db_filename = os.path.abspath('sqlitePath')

        self.goalClass.createTable(True)

    def reCreateTable(self):
        self.goalClass.dropTable(True)
        self.goalClass.createTable()

    def add(self, p):

        if hasattr(self.goalClass, 'info_createTime'):
            p['info_createTime'] = DateTimeCol.now()
            # .strftime('%Y-%m-%d %H:%M:%S.%f')

        self.goalClass(**p)

    def addAll(self, items):
        for item in items:
            self.add(item)

    def exportTxt(self, dirName, getFileName, getFileContent, selectP,encoding = 'utf-8'):

        tz.mkDir(dirName)

        objs = self.goalClass.select(selectP)

        successCount = 0
        wrongCount = 0
        wrongs = []

        for ele in objs:
            fileName = getFileName(ele).decode(encoding)
            content = getFileContent(ele).decode(encoding)

            try:
                tz.writeFile(dirName + '/%s.txt' % fileName, content)
                successCount += 1
            except Exception,e:
                wrongCount += 1
                wrongs.append(fileName)
                traceback.print_exc()
                # raise e

        lenT = objs.count()
        print '%d/%d,%d failed @ %s'%(successCount,lenT,wrongCount,wrongs)


    @classmethod
    def commit(cls):
        cls.connection.getConnection().commit()


if __name__ == '__main__':
    # DataWrapper.initDb('dataT/data.db')
    #
    # wrapper = DataWrapper('t', DataWrapper.wrappeByCommonFieldCfg({'content': StringCol()}))
    #
    # # wrapper.reCreateTable()
    #
    # # wrapper.add(name = 'b')
    # wrapper.add({'name': 'a', 'content': u'中文'})

    print u'中文'

