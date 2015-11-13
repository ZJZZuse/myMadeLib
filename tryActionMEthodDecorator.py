#coding=utf-8
'''
try 装饰器
'''


__author__ = 'wb-zhangjinzhong'

import traceback


def tryAction(action, times=3):
    '''

    :param action: 参数在外面直接用lambda封装
    :param times:
    :return:
    '''

    for i in range(0, times):

        if i > 0:
            print 'tried %s time(s)' % i

        try:
            return action()
        except Exception, e:
            traceback.print_exc()

    # print 'failed,after having tried %s time(s)' % times

    raise Exception('tryActionExcetion,failed,after having tried %s time(s)' % times)

def tryActionMEthod(times):
    '''
    装饰器
    :param times: 次数
    :return:
    '''
    def tryActionOuter(fn):

        def goalFn(*args, **kwargs):

            fnT = lambda : fn(*args, **kwargs)

            return tryAction(fnT, times)

        return goalFn

    return tryActionOuter
