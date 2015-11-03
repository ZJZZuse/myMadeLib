# encoding=utf-8
__author__ = 'Zhang'

import sys
import os
import codecs

typeEncode = sys.getfilesystemencoding()  ##系统默认编码

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


def decodeForThisSys(content,encoding='gb2312'):
    return content.decode(encoding,'ignore').encode(typeEncode)

def commonErrorPrint(e):
    s = sys.exc_info()
    print "%s,Error '%s' happened on line %d" % (e.__class__, s[1], s[2].tb_lineno)

def writeFile(path, text,encoding = 'utf-8', passIfExist=True):
    if passIfExist and os.path.exists(path):
        return

    with codecs.open(path, 'w',encoding)  as f:  # r只读，w可写，a追加
        f.write(text)

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


def tryMkdir(dirName, times=3):
    for i in (0, times):

        if i > 0:
            print 'now index is %d' % i

        try:
            os.mkdir(dirName)
            return True
        except Exception, e:
            print e, 'at make dir %s' % dirName

    return False
