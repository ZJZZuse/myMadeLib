# coding=utf-8
__author__ = 'wb-zhangjinzhong'


class MySpiderCfg:
    '''
    自有蜘蛛简单配置类
    '''
    name = 'default'

    baseUrl = '基础地址，通常用于页面省略地址补全'
    mainActionUrl = 'http://yhyz.6000y.com/news/news_140_%d.html'
    baseFilePath = 'F:/more/illusion/other/ling/other/text/aisirenText2/%s.txt'

    def __init__(self, name, baseUrl, mainActionUrl, baseFilePath):
        '''

        :param name:
        :param baseUrl:
        :param mainActionUrl:
        :param baseFilePath:
        :return:
        '''

        self.baseUrl = baseUrl
        self.mainActionUrl = mainActionUrl
        self.baseFilePath = baseFilePath
        self.name = name
