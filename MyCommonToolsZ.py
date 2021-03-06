# encoding=utf-8
__author__ = 'Zhang'

import sys
import os
import codecs
import tryActionMEthodDecorator

typeEncode = sys.getfilesystemencoding()  ##系统默认编码

def fireActionTimes(fn, times = 1):
    '''
    执行fn相应的次数
    :param fn:
    :param times:
    :return:
    '''
    for i in range(0, times):
        fn()


def emptyOrNoneAll(*items):
    '''
    全部为空？
    :param items:
    :return:
    '''
    for ele in items:
        if not(ele == None or ele == ''):
            return False

    return True


def decodeForThisSys(content,errors = 'ignore',encodeErrors = 'strict',encoding='gb2312'):
    return content.decode(encoding,errors).encode(typeEncode,encodeErrors)

def decodeMy(content,gEncode  = 'gb2312',goalEncode = 'utf-8'):
    return content.decode(gEncode).encode(goalEncode)

def commonErrorPrint(e):
    s = sys.exc_info()
    print "%s,Error '%s' happened on line %d" % (e.__class__, s[1], s[2].tb_lineno)

def writeFile(path, text,encoding = 'utf-8', passIfExist=True):
    if passIfExist and os.path.exists(path):
        return

    with codecs.open(path, 'w',encoding)  as f:  # r只读，w可写，a追加
        f.write(text)

def replaceCRLF(content):
    return content.replace('\n','\r\n')

def mkDir(dirName, passIfExist = True):
    '''
    创建文件夹
    :param dirName:
    :param passIfExist:
    :return:创建了？,存在放回false
    '''
    if passIfExist and os.path.exists(dirName):
        return False

    os.mkdir(dirName)
    return True

@tryActionMEthodDecorator.tryActionMEthod(3)
def tryMkdir(dirName, passIfExist = True):
     return mkDir(dirName, passIfExist)

# def tryMkdir(dirName, times=3):
#     for i in (0, times):
#
#         if i > 0:
#             print 'now index is %d' % i
#
#         try:
#             os.mkdir(dirName)
#             return True
#         except Exception, e:
#             print e, 'at make dir %s' % dirName
#
#     return False

if __name__=='__main__':
    writeFile(u'D:/data/text/askTao/中文.txt',u'a中文\r\na')