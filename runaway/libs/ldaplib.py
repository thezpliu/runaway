#!/usr/bin/env python
# encoding=utf-8

import ldap
from cfg import conf
import re


ldapuser = conf.ldapConfig['ldapuser']
ldappass = conf.ldapConfig['ldappass']
ldappath = conf.ldapConfig['ldappath']
baseDN = conf.ldapConfig['baseDN']
LDAP_BASE_DN = 'dc=z,dc=liu'


def _validateLDAPUser(user, qtype='uid'):
    try:
        l = ldap.initialize(ldappath)
        l.protocol_version = ldap.VERSION3
        l.simple_bind(ldapuser, ldappass)

        searchScope = ldap.SCOPE_SUBTREE
        searchFiltername = qtype
        retrieveAttributes = None
        # None 表示搜索所有属性
        searchFilter = '(' + searchFiltername + "=" + user + ')'
        ldap_result_id = l.search(baseDN, searchScope, searchFilter,
                                  retrieveAttributes)
        result_type, result_data = l.result(ldap_result_id, 1)
        if (not len(result_data) == 0):
            return result_data
        else:
            return False
    except Exception:
        return False
    finally:
        l.unbind()
        del l


def validateLDAPUser(user='', qtype='cn', trynum=8):
    i = 0
    foundResult = ""
    while (i < trynum):
        foundResult = _validateLDAPUser(user=user, qtype=qtype)
        if (foundResult):
            return foundResult
        i += 1
    return False

def get_mobile_by_cn(cn=''):
    r = validateLDAPUser(user=cn, qtype='cn')
    if not r:
        return None
    return r[0][1]['uid'][0]


def get_mail_by_cn(cn=''):
    r = validateLDAPUser(user=cn, qtype='cn')
    if not r:
        return None
    return r[0][1]['mail'][0]

def ldapList(filterstr='(objectClass=*)', attrib=None, scope=ldap.SCOPE_SUBTREE):
    l = ldap.initialize(ldappath)
    l.protocol_version = ldap.VERSION3
    l.simple_bind(ldapuser, ldappass)
    s = l.search_s(baseDN, scope,filterstr,attrlist=attrib)
    user_group = {}
    for item in s:
        attrib_dict0 = item[0]
        attrib_dict1 = item[1]

        if attrib_dict1.has_key('userPassword'):
            user_info = []
            user_ou = attrib_dict0.split(',')[1].replace('ou=','').decode('utf-8')
            if attrib_dict1.has_key('cn'):
                user_name = attrib_dict1['cn'][0]
            if attrib_dict1.has_key('uid'):
                user_phone = attrib_dict1['uid'][0]
            else:
                user_phone = ''
            if attrib_dict1.has_key('mail'):
                user_email = attrib_dict1['mail'][0]
            else:
                user_email = ''
            if user_group.has_key(user_ou):
                user_info.append(user_phone)
                user_info.append(user_email)
                user_group[user_ou][user_name] = user_info
            else:
                user = {}
                user_info.append(user_phone)
                user_info.append(user_email)
                user[user_name] = user_info
                user_group[user_ou] = user

    return user_group
def ldap_update_pass(user=None,oldpass=None,newpass=None):
    print oldpass
    l = ldap.initialize(ldappath)
    l.protocol_version = ldap.VERSION3
    l.simple_bind(ldapuser, ldappass)
    searchFilter = "cn=" + user
    s = l.search_s(baseDN, ldap.SCOPE_SUBTREE,searchFilter,None)[0][0]
    try:
        l.passwd_s(s, oldpass, newpass)
        return True
    except ldap.LDAPError,e:
        return e
if __name__ == "__main__":
	r = validateLDAPUser('flat')
	print "result:",r
	print "group:",(str(r[0][0]).split(',')[1]).split('=')[1]
	print r[0][1]['cn'][0]
