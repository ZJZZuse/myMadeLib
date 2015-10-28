# encoding=utf-8
__author__ = 'Zhang'

import sys


class MyCommonToolsZ:
    '''
    commonErrorPrint
    '''
    @staticmethod
    def commonErrorPrint(e):
        s = sys.exc_info()
        print "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)

