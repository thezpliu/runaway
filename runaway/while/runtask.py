#!/usr/bin/env python
# encoding=utf-8

from multiprocessing import Process
import Queue
import time
import sys
import os
import signal
import random

# 加载环境变量
CLIDIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(os.path.dirname(CLIDIR))
path = ROOT
sys.path.append(path)
from runaway.libs.daemon import Daemon
from runaway.libs.cfg import conf
from wcache import monitor_cache,svninfo_cache,p4_cache
from runaway.libs.log import logd
def sub_process():
	try:
    		signal.signal(signal.SIGCHLD, signal.SIG_IGN)
		#SIGCHLD信号是在子进程退出时或是状态发送变化时发送给父进程的。父进程会用wait或waitpid来处理这个信号，在处理之前子进程为僵尸状态
		#设置成signal.SIG_IGN 的意思是父进程不去管理子进程，子进程由系统init进程管理(wait)。
        	m = Process(target=monitor_cache, args=[5])
        	s = Process(target=svninfo_cache, args=[300])
        	n = Process(target=p4_cache, args=[300])
        	m.start()
        	s.start()
        	n.start()
    	except Exception as e:
		logd.sys_log_save(e.message)
class TaskDaemon(Daemon):
    def _run(self):
	sub_process()
if __name__ == '__main__':
    print("pidpath",conf.whileConfig['pid_path'] + 'runawayd.pid')
    daemon = TaskDaemon(conf.whileConfig['pid_path'] + 'runawayd.pid')
    if len(sys.argv) == 2:
        if 'START' == (sys.argv[1]).upper():
            daemon.start()
        elif 'STOP' == (sys.argv[1]).upper():
            daemon.stop()
        elif 'RESTART' == (sys.argv[1]).upper():
            daemon.restart()
        else:
            print "Unknow Command!"
            print "Usage: %s start|stop|restart" % sys.argv[0]
            sys.exit(2)
        sys.exit(0)
    else:
        print "Usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(0)
