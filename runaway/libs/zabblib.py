#!/usr/bin/env python
# encoding=utf-8
from cfg import conf
import json
import urllib2
import re
from log import logd
class zabbix_api(object):
	def __init__(self,zabbix_id):
		'''获取访问zabbix api的令牌'''
		self.iid = zabbix_id
		url = 'zabbix_url' + str(zabbix_id)
		admin = 'zabbix_admin' + str(zabbix_id)
		passwd = 'zabbix_password' + str(zabbix_id)
		self.url = conf.zabbixconfig[url]
		values = {
				'jsonrpc': '2.0',
                        	'method': 'user.login',
                        	'params': {
                        		'user': conf.zabbixconfig[admin],
                        		'password': conf.zabbixconfig[passwd]
                        		},
                        	'id': '0'
                	}
		res =  self.zabbix_request(values)
		logd.sys_log_save('get zabbix api auth success',1)
		if res != None:	
			self.auth = res['result']
		else:
			self.auth = None
	def zabbix_request(self,values):
    		data = json.dumps(values)
		req = urllib2.Request(self.url,data,{'Content-Type': 'application/json-rpc'})
    		try:
			response = urllib2.urlopen(req, data)
    			output = json.loads(response.read())
    			return output
    		except Exception as e:
			logd.sys_log_save(e)
			return None
	def zabbix_host(self):
		'''获取主机'''
		values = {
				'jsonrpc': '2.0',
    				"method": "host.get",
    				"params": {
        					"output": 		"extend",
						"selectInterfaces":     ["ip"],
                                                "selectGroups":         "groupids",
						"selectParentTemplates": ["templated_hosts","templateids"]
    						},
    				"id": 1,
    				"auth": self.auth
                	}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_cr_host(self,hostname,ip,port,template,groupid):
		'''创建主机'''
		values = {
			"jsonrpc": "2.0",
    			"method": "host.create",
    			"params": {
        			"host": hostname,
        			"interfaces": [
            					{
                					"type": 1,
                					"main": 1,
                					"useip": 1,
                					"ip": ip,
                					"dns": "",
                					"port": port
            					}
        					],
        			"groups": [
            					{
                					"groupid": groupid
            					}
        				],
        			"templates": [template],
        			"inventory_mode": 0,
        			"inventory": {
        			}
    			},
    			"auth": self.auth,
    			"id": 101
                	}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_cr_item(self,hostid,itemname,key):
		'''创建监控项目'''
        	values = {
		    	"jsonrpc": "2.0",
    			"method": "item.create",
    			"params": {
        			"name": itemname,
        			"key_": key,
        			"hostid": hostid,
        			"type": 0,
        			"value_type": 3,
        			"interfaceid": "1",
        			"delay": 30
    				},
    			"auth": self.auth,
    			"id": 2
		}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_cr_trigger(self,experssion):
		'''创建触发器'''
		values = {
			"jsonrpc": "2.0",
    			"method": "trigger.create",
    			"params": [
        				{
            					"description": "Processor load is too high on {HOST.NAME}",
            					"expression": experssion,
        				},
    				],
    			"auth": self.auth,
    			"id": 10
			}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_enable_item(self,itemid):
		'''启动监控项'''
        	values = {
			"jsonrpc": "2.0",
			"method": "item.update",
			"params": {
				"itemid": itemid,
				"status": 0
				},
    			"auth": self.auth,
    			"id": 3
                }
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None

	def zabbix_enable_trigger(self,triggerid):
		'''启动触发器'''
        	values = {
			"jsonrpc": "2.0",
    			"method": "trigger.update",
    			"params": [
        				{
            					"triggerid": triggerid,
            					"status": 0
        				},
    				],
    			"auth": self.auth,
    			"id": 11
                }
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_trigger_get(self,hostids):
		'''获取报警项目'''
		values = {	'jsonrpc': '2.0',
           		"method":"trigger.get",
               		"params": {
                        	"output":"extend",
				'hostids' : hostids,
				"filter": {
            				"value": 1
        				},
				"selectFunctions": "extend",
             	 		"sortfield": "priority",
              			"sortorder": "DESC"
            		},
              		'auth': self.auth,
              		'id': '4'
              	}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_event_get(self,hostids):
		values = {
			    "jsonrpc": "2.0",
			    "method": "event.get",
			    "params": {
			    	"hostids": hostids,
			        "output": "extend",
			    	"value": 1,
				"select_alerts" : "extend",
			        "select_acknowledges": "extend",
			        "sortfield": ["clock", "eventid"],
			        "sortorder": "DESC"
				 },
				"auth": self.auth,
 				"id": 8
			}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_items_value(self,itemid):
		'''获取监控项最新值'''
		values = {	'jsonrpc': '2.0',
              		'method': "history.get",
              		"params": {
                    			"output": "extend",
                    			"history":3,
                    			"itemids":itemid,
                    			"sortfield": "clock",
                    			"sortorder": "DESC",
                    			"limit":1,
                			},

              		'auth': self.auth,
              		'id': '5'
              		}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_hostid_get(self,ip):
		'''通过IP获取主机HOSTID'''
		values = {	
			'jsonrpc': '2.0',
              		'method': 'host.get',
              		'params': {
                  		'output': [ "host" ], 
                  		'filter': {
                      			'ip': ip
                  			},
              			},
              		'auth': self.auth,
              		'id': '6'
              	}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
	def zabbix_itemid_get(self,hostid):
		'''通过主机ID获取监控项ID'''
		values = {
			'jsonrpc': '2.0',
              		'method': "item.get",
              		"params": {
                    			"output": ["name","lastvalue","key_"],
                    			#"output": "extend",
                    			"hostids": hostid,
					"filter": {
						"key_": ["net.if.in[enp4s0]","net.if.out[enp4s0]","system.cpu.util[,iowait]","system.cpu.load[percpu,avg1]","system.cpu.load[percpu,avg5]","system.cpu.load[percpu,avg15]","proc.num[,,run]","vm.memory.size[free]","vm.memory.size[available]","vm.memory.size[total]","net.if.in[eth0]","net.if.out[eth0]","vfs.fs.size[/,pfree]","vfs.fs.size[/home/SiriusData,pfree]","vfs.fs.size[/home/data,pfree]","vfs.fs.size[/home,pfree]","net.if.in[Broadcom NetXtreme Gigabit Ethernet]","net.if.out[Broadcom NetXtreme Gigabit Ethernet]","vfs.fs.size[C:,pfree]","vfs.fs.size[D:,pfree]","vfs.fs.size[E:,pfree]"]
					}
                		},
              		'auth': self.auth,
              		'id': '7'
              		}
		if self.auth != None:
			res =  self.zabbix_request(values)
			if res != None:
				return res['result']
			else:
				return None
		else:
			return None
zapi1 = zabbix_api(0)
zapi2 = zabbix_api(1)
