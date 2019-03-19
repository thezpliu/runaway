#!/usr/bin/env python
# encoding=utf-8
from runaway.libs.cfg import conf
from runaway.libs.zabblib import zapi1,zapi2
from runaway.libs.log import logd
import json
import re
def get_items(inf=0):
	zab = [zapi1,zapi2]
       	resultlist = []
        for za in zab:
		try:
        	       	for host in za.zabbix_host():
        	        	       	hostinfo = {}
					hostinfo['iid'] = za.iid
					hostinfo['id'] = host['hostid']
        	        	       	hostinfo['name'] = host['name']
        	        	       	hostinfo['ip'] = host['interfaces'][0]['ip']
					if inf == 0:
        	        	       		for items in za.zabbix_itemid_get(host['hostid']):
        	        	       			hostinfo[items['key_']] = items['lastvalue']
        					resultlist.append(hostinfo)
					elif inf == 1:
						eventlist = []
						for event in za.zabbix_event_get(host['hostid']):
							eventlist.append(event)
						hostinfo['event'] = eventlist
					 	resultlist.append(hostinfo)
		except Exception as e:
			logd.sys_log_save(e.message)
			continue
	return resultlist
def get_item():
	load = re.compile(r'system.cpu.load')
	disk = re.compile(r'vfs.fs.size')
	net = re.compile(r'net.if')
	netoutput = re.compile(r'net.if')
	memory = re.compile(r'vm.memory.size')
	process = re.compile(r'proc.num')
	spec = re.compile('((?:\w+.){1,2}\w+)\[(\S+|(?:\S+\s)+\S+)\]')
	seg = re.compile(r',')
	dot = re.compile("\.")
	notp = re.compile('^p')
	slash = re.compile(r'/')
	colon = re.compile(r':')
	avg = re.compile(r'avg')
	allkeys = []
	allinfo = []
	resultl = get_items(0)
	if resultl:
	        for res in resultl:
			allitems = {}
			disks = ''
			for k,v in res.items():
				if load.match(k):
					if seg.split(re.match(spec,k).group(2))[1] == 'avg1':
						avg1 = v
					if seg.split(re.match(spec,k).group(2))[1] == 'avg5':
						avg5 = v
					if seg.split(re.match(spec,k).group(2))[1] == 'avg15':
						avg15 = v
				elif disk.match(k):
					diskname = seg.split(re.match(spec,k).group(2))[0]
					diskspace = diskname + ' : ' + str(round(float(v))) + '%  '
					disks = disks + ' ' + diskspace + ' '
				elif net.match(k):
					drive = seg.split(re.match(spec,k).group(2))[0]
					if seg.split(re.match(spec,k).group(1))[0] == 'net.if.in':
						netin = v
					if seg.split(re.match(spec,k).group(1))[0] == 'net.if.out':
						netout = v
				elif memory.match(k):
					if seg.split(re.match(spec,k).group(2))[0] == 'total':
						memtotal = v
					else:
						memfree = v
				elif k == 'name':
					allitems['name'] = v
				elif k == 'id':
					allid = v
				elif k == 'iid':
					iid = v
				elif k == 'ip':
					allip = v
			allitems['network'] = 'NULL'
			if netout:
				allitems['netout'] = int(netout) / 8
			if netin:
				allitems['netin'] = int(netin) / 8
			allitems['mem'] = str(int(memtotal) / 1024 / 1024) +  'MB /' + str(int(memfree) / 1024 / 1024 ) + 'MB'
			allitems['load'] = avg1 + ' | ' + avg5 + ' | ' + avg15
			allitems['disk'] = disks
			allitems['id'] = allid + str(iid)
			allitems['ip'] = allip
			allinfo.append(allitems)
		return allinfo
	else:
		return None
if __name__ == "__main__":
	pass
