#!/usr/bin/env python
# encoding=utf-8
'''
日志类模块
'''

import os
import sys
import time
from cfg import conf

class Log():
    """some function for log"""

    def __init__(self):
        pass

    def get_time(self, flag=0):
        '''
        获取时间
        @flag: 默认为0，返回年月日，如1900-10-10; 其他返回如1900-10-10 10:10:10
        '''
        if flag:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        else:
            return time.strftime('%Y-%m-%d', time.localtime())

    def sys_log_save(self, logstr='', leaval=3):
        if logstr == '':
            return
        logstr = str(logstr)
        logleaval = 'INFO'

        if leaval == 0:
            logleaval = 'INFO'
        elif leaval == 1:
            logleaval = 'DEBUG'
        elif leaval == 2:
            logleaval = 'WARNING'
        elif leaval == 3:
            logleaval = 'ERROR'

        sblank = ' '
        src = 'runaway'
        logSeq = (self.get_time(1), logleaval, logstr)
        logstr = sblank.join(logSeq)

        lineno = sys._getframe().f_back.f_lineno

        co_name = sys._getframe().f_back.f_code.co_name

        file_name = sys._getframe().f_back.f_code.co_filename
        if leaval == 3:
            detailLogSeq = ('\nfile name:', str(file_name),
                            ',function name:', str(co_name),
                            ',line:', str(lineno))
            logdetail = ''.join(detailLogSeq)
            logstr = logstr + logdetail

        print logstr

        if leaval < conf.config['log_leaval']:
            return

        logdirSeq = (conf.config['sys_log_path'], os.sep)

        logdir = ''.join(logdirSeq)

        if not os.path.exists(logdir):
            os.system('mkdir -p %s' % (logdir))

        logfile = logdir + conf.config['sys_log_name'] + '_' + str(self.get_time()) + '.log'

        try:
            f = open(logfile, 'a+')
            f.write(logstr + '\n')
            f.close
        except Exception as e:
            print e

logd = Log()
if __name__ == "__main__":
    '''
    log = Log()
    log.sys_log_save('bbbb')
    '''
    pass
