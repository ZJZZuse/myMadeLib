# coding=utf-8
__author__ = 'wb-zhangjinzhong'


class MySpiderCfg(object):
    '''
    自有蜘蛛简单配置类
    '''
    name = 'default'
    baseUrl = '基础地址，通常用于页面省略地址补全'

    specialMainActionUrl = ()

    mainActionUrl = False
    # such as mainActionUrls = ({'url': '', 'range': range(1,3 + 1)},)
    mainActionUrls = ()

    baseFilePath = 'F:/more/%s.txt'

    def __init__(self, p):

        for key in p:
            self.__setattr__(key,p[key])

        self._generateIter()

    def _generateIter(self):
        self.iter = self.generateIter()
        if not self.mainActionUrl:
            self.iter = self.generateIterCommon()

    def generateIterCommon(self):
        for ele in self.specialMainActionUrl:
            yield ele

        for actionObj in self.mainActionUrls:
            for i in actionObj['range']:
                yield actionObj['url'] % i

    def generateIter(self):

        for ele in self.specialMainActionUrl:
            yield ele

        for i in self.range:
            yield self.mainActionUrl % i


if __name__ == '__main__':
    print 1
    pass
    # objT = {
    #     'a': 1,
    #     'b': 2
    #     ,
    #     'c': 3
    #
    # }
    #
    # for key in objT:
    #     print objT[key]

    # o = MySpiderCfg('a')
    # print o.baseUrl


