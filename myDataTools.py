# coding=utf-8
__author__ = 'wb-zhangjinzhong'

from sqlobject import *
from new import classobj

import os


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
        'name': StringCol(),
        '_createTime': DateTimeCol()
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

        sqlhub.processConnection = connection


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

        if hasattr(self.goalClass, '_createTime'):
            p['_createTime'] = DateTimeCol.now()

        self.goalClass(**p)

    def addAll(self, items):
        for item in items:
            self.add(item)


if __name__ == '__main__':
    DataWrapper.initDb('dataT/data.db')

    wrapper = DataWrapper('t', DataWrapper.wrappeByCommonFieldCfg({'content': StringCol()}))

    # wrapper.reCreateTable()

    # wrapper.add(name = 'b')
    wrapper.add({'name': 'a', 'content': u'中文'})
