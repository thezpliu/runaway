#!/usr/bin/env python
# encoding=utf-8
'''
monitor views
'''
from flask import render_template as temp
from runaway.libs.cfg import conf
from runaway.models.mlogin import logincheck, sib_login
from runaway.libs.ldaplib import ldapList
from flask import session
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")
@logincheck
def p4_v():
	return temp("p4info.html")
