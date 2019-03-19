#!/usr/bin/env python

import os,re,json
import shlex
import subprocess
from cfg import conf
from log import logd
def getsvninfo(host,repo):
	user = 'baoyong234'
	line = re.compile('\n')
	colon = re.compile(r':')
	repoaddr = "/usr/bin/svn info svn+ssh://" + user + "@" + host + '/' + repo
	s = subprocess.Popen(repoaddr,shell=True,stdout=subprocess.PIPE)
	checkback = """/usr/bin/ssh -i /root/.ssh/id_dsa root@192.168.0.231 "/usr/bin/svnlook youngest /var/svn/{0}" """.format(repo)
	b = subprocess.Popen(checkback,shell=True,stdout=subprocess.PIPE)
	s.wait()
	b.wait()
	ue = s.communicate()
	be = b.communicate()
	svninfo_d = {}
	if ue[1] == None:
		x = line.split(ue[0].strip('\n'))
		for y in x:
			svninfo_d[colon.split(y)[0]] = ':'.join(colon.split(y)[1:])
		if be[1] == None:
			svninfo_d['back'] = be[0]
		else:
			svninfo_d['back'] = 'unknow'
	else:
		logd.sys_log_save(ue[1])
		svninfo_d['error'] = ue[1]
		if be[1] == None:
			svninfo_d['back'] = be[0]
		else:
			svninfo_d['back'] = 'unknow'
	return svninfo_d
if __name__ == '__main__':
	#host = '192.168.1.33'
	#print json.dumps(getsvninfo(host,repo),indent=3)
	pass
