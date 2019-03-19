#!/usr/bin/env python
import redis
from cfg import conf
from log import logd
class rRedis(object):
	def __init__(self,host,port,db=1,password=''):
		self.host = host
		self.port = port
		self.db = db
		self.password = password
		try:
			self.pool = redis.ConnectionPool(host=self.host,port=self.port,db=self.db)
			self.r = redis.Redis(connection_pool=self.pool)
			self.p = self.r.pipeline()
			logd.sys_log_save('redis connect success',1)
		except Exception,e:
			logd.sys_log_save(e.message)
	def getC(self):
		allinfo = []
		for i in self.r.keys():
			allinfo.append(self.r.hgetall(i))
		return allinfo
	def getk(self):
		return self.r.keys()
	def gethk(self,n,k):
		if self.r.exists(n):
			if self.r.hexists(n,k):
				return self.r.hget(n,k)
			else:
				return None
		else:
			return None
rb1 = rRedis(host=conf.redisConfig['host'],port=conf.redisConfig['port'],db=1,password=conf.redisConfig['password'])
rb2 = rRedis(host=conf.redisConfig['host'],port=conf.redisConfig['port'],db=2,password=conf.redisConfig['password'])
rb3 = rRedis(host=conf.redisConfig['host'],port=conf.redisConfig['port'],db=3,password=conf.redisConfig['password'])
