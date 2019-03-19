#!/usr/bin/env python
from P4 import P4,P4Exception
from cfg import conf
from log import logd
p4 = P4()
def getp4info(port):
	try:
		p4.port = conf.p4Config['host'] + ':' + port
		p4.user = conf.p4Config['user']
		p4.password = conf.p4Config['password']
    		p4.connect()
		p4.run_login()
    		x = p4.run('changelists','-m 1')[0]
    		p4.disconnect()
	except Exception as e:
    		logd.sys_log_save(e)
		x = None
	try:
		p4.port = conf.p4Config['backhost'] + ':' + port
		p4.user = conf.p4Config['user']
		p4.password = conf.p4Config['password']
    		p4.connect()
		p4.run_login()
    		y = p4.run('changelists','-m 1')[0]
    		#logd.sys_log_save(y,1)
    		p4.disconnect()
	except Exception as e:
    		logd.sys_log_save(e)
		y = None
	return x,y
if __name__ == '__main__':
	#x,y = getp4info("1840")
	#print x,y
	pass
