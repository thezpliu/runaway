#!/usr/bin/env python
from monitor import get_item
from runaway.libs.redislib import rb1,rb2,rb3
from runaway.libs.svnlib import getsvninfo
from runaway.libs.p4lib import getp4info
from runaway.libs.cfg import conf
from runaway.libs.log import logd
import time,chardet,json
def monitor_cache(sec):
	while True:
		g = get_item()
		if g:
			for i in g:
				name = i['id']
				if rb1.r.hexists(name,'netin'):
					if int(i['netin']) > 9999999:
						innum = str(format( float(i['netin']) / float(1048576),'.1f')) + ' MB'
					else:
						innum = str(format(float(i['netin']) / float(1024),'.1f')) + ' KB'
					if int(i['netout']) > 9999999:
						outnum = str(format(float(i['netout']) / float(1048576),'.1f')) + ' MB'
					else:
						outnum = str(format(float(i['netout']) / float(1024),'.1f')) + ' KB'
					i['network'] = innum + ' / '  + outnum
					if name == '101050':
						logd.sys_log_save("innum:"+str(innum),1)
						logd.sys_log_save("outnum:"+str(outnum),1)
						logd.sys_log_save("netin:"+str(i['netin']),1)
						logd.sys_log_save("netout:"+str(i['netout']),1)
				rb1.p.hmset(name,i)
        			rb1.p.expire(name,30)
			x = rb1.p.execute()
			logd.sys_log_save('get zabbix info success',1)
			time.sleep(sec)
		else:
			logd.sys_log_save('get zabbix info faild')
			time.sleep(2)
def svninfo_cache(sec):
	host = conf.svnConfig['host']
	repolist = conf.svnConfig['repolist']
	while True:
		for re in repolist:
			try:
				sd = getsvninfo(host,re)
				if 'error' in sd.keys():
					sd['Node Kind'] = 'error'
					sd['URL'] = 'error'
					sd['Last Changed Date'] = 'error'
					sd['Repository Root'] = 'error'
					sd['back'] = 'error'
					sd['Last Changed Author'] = 'error'
					sd['Path'] = re
					sd['Revision'] = 'error'
					sd['Last Changed Rev'] = 'error'
					sd['Repository UUID'] = 'error'
				rb2.p.hmset(re,sd)
        			rb2.p.expire(re,600)
			except Exception as e:
				logd.sys_log_save(e)
				pass
		try:
			x = rb2.p.execute()
		except Exception as e:
			logd.sys_log_save(e)
			pass
		time.sleep(sec)
def p4_cache(sec):
	portlist = conf.p4Config['portlist']
	while True:
		for port in portlist:
			try:
				x,e = getp4info(port)
				if x:
					y = x.copy()
					last = time.localtime(float(y['time']))
					y['times'] = time.strftime('%Y-%m-%d %H:%M:%S',last)
					y['port'] = port
					y['path'] = ''
					y['desc'] = ''
					i18 = chardet.detect(y['client'])
					if i18['encoding'] != 'ascii':
						ilog = i18['encoding'] + '--' + y['client'] + '--' + y['port']
						y['client'] = y['client'].decode('ISO-8859-1')
						logd.sys_log_save(ilog)
					if x == e:
						y['back'] = 'yes'
					else:
						if e:
							y['back'] = e['change']
						else:
							y['back'] = 'error'
				else:
					y["status"] = "error"
					y["changeType"] = "error"
					y["times"] = "error"
					y["client"] = "error"
					y["user"] = "error"
					y["time"] = "error"
					y["path"] = "error"
					y["port"] = port
					y["change"] = "error"
					y["desc"] = "error"
					if e:
						y["back"] = e["change"]
					else:
						y["back"] = "error"
				rb3.p.hmset(port,y)
        			rb3.p.expire(port,600)
			except Exception as e:
				logd.sys_log_save(e)
				pass
		try:
			rb3.p.execute()
		except:
			pass
		time.sleep(sec)
