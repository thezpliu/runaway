#!/usr/bin/env python
# encoding=utf-8
import re
from flask_restful import Resource
from flask import request
from runaway.libs.redislib import rb1
class zabbix_info(Resource):
	def get(self):
		return rb1.getC()
