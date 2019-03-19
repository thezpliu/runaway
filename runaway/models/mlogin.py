#!/usr/bin/env python
# encoding=utf-8
'''
logs model
'''
from runaway.libs.cfg import conf
from runaway.libs.ldaplib import validateLDAPUser
from flask import session, url_for, redirect
from base64 import b64encode
import sha
import hashlib
from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode
from flask import request
import os
import time
import ldap
class Login(object):
    """Login model class"""

    def __init__(self):
        self.config = conf.config
        self.ldapuser = conf.ldapConfig['ldapuser']
        self.ldappass = conf.ldapConfig['ldappass']
        self.ldappath = conf.ldapConfig['ldappath']
        self.baseDN = conf.ldapConfig['baseDN']
        self.LDAP_BASE_DN = 'dc=z,dc=liu'

    def check_user_pass(self, user='', password=''):
        if not user or not password:
            return 'empty'
        r = validateLDAPUser(user=user, qtype='cn') 
	# 搜索user的在LDAP里的所有信息都包含在r里
        if r and self.ldaplogin(user,password):
	#self.ldaplogin(user,password)这个方法验证用户密码是否能登录。
            cn = r[0][1]['cn'][0]
            session['user'] = cn
            session['user_group'] = (str(r[0][0]).split(',')[1]).split('=')[1]
            return True, cn
        return False, 'Guest'
    def is_login(self):
        if not session:
            return False
        if session['user'] != '':
            return True
        return False

    def login_out(self):
        session['user'] = session['user_group'] = ''
        del session['user']
        del session['user_group']
    def ldaplogin(self,user,passwd):
        l = ldap.initialize(self.ldappath)
        l.protocol_version = ldap.VERSION3
        l.simple_bind(self.ldapuser, self.ldappass)
        searchfilter = "cn=" + user
        s = l.search_s(self.baseDN, ldap.SCOPE_SUBTREE, searchfilter,None)[0][0]
        try:
            my_ldap = ldap.initialize(self.ldappath)
            my_ldap.simple_bind_s(s, passwd)
            return True
        except:
            return False

sib_login = Login()


def logincheck(func):
    def wrapper(*args, **kwargs):
        if sib_login.is_login() is False:
            return redirect(url_for('login'))
        r = func(*args, **kwargs)
        return r

    return wrapper

if __name__ == "__main__":
    pass
