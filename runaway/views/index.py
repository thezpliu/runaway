#!/usr/bin/env python
# encoding=utf-8
'''
index views
'''
from flask import render_template as temp
from runaway.libs.cfg import conf
from runaway.models.mlogin import logincheck, sib_login
#from runaway.libs.db import Db
from runaway.libs.ldaplib import ldapList
from flask import session
import sys
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )
@logincheck
def index():
    # runaway index page
    return temp('base.html')
