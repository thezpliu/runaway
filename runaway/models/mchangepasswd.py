#!/usr/bin/env python
# encoding=utf-8
import time
from flask import session
import sys
import time
from runaway.libs.ldaplib import ldap_update_pass
reload(sys)
sys.setdefaultencoding( "utf-8" )
class changepasswd(object):
    """docstring for Task"""
    def __init__(self):
        self.user = session['user']
    def update_passwd(self, data):
        oldpasswd = eval(data)['oldpasswd']
        newpasswd = eval(data)['newpasswd']
        res = ldap_update_pass(self.user, oldpasswd, newpasswd)
        if res is True:
            return 0
        else:
            return 1

