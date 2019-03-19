# coding=utf-8
from runaway.views.index import index
from runaway.views.login import login, user_login_out
from runaway.views.monitor import monitor
from runaway.views.svninfo import svn_v
from runaway.views.p4info import p4_v
from runaway.api.ldap_login import LoginCheck
from runaway.api.changepasswd import ChangePasswd
from runaway.api.zabbix import zabbix_info
from runaway.api.svninfo import svn_info
from runaway.api.p4info import p4_info
APIURL = [
    [LoginCheck, '/api/v1/login'],
    [ChangePasswd, '/api/v1/changepasswd'],
    [zabbix_info,'/api/v1/zabbix_info'],
    [svn_info,'/api/v1/svn_info'],
    [p4_info,'/api/v1/p4_info'],
]

URLS = [
    ['/', 'index', 'GET', index],
    ['/login', 'login', 'GET', login],
    ['/user_login_out/', 'user_login_out', 'GET', user_login_out],
    ['/monitor', 'monitor', 'GET', monitor],
    ['/svninfo', 'svninfo', 'GET', svn_v],
    ['/p4info', 'p4info', 'GET', p4_v],
]

def regist_urls(app=None, api=None):
    if app is None or api is None:
        return
    for url in APIURL:
        api.add_resource(url[0], url[1])
    for url in URLS:

        if url[2].find(',') > 0:
            mlist = url[2].split(',')
        else:
            mlist = [url[2]]

        app.add_url_rule(rule=url[0], endpoint=url[1],
                         methods=mlist, view_func=url[3])
