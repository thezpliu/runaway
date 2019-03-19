#!/usr/bin/env python
# encoding=utf-8
'''
login views
'''
from flask import render_template as temp
from flask import session, redirect, url_for, request
from runaway.libs.cfg import conf
from runaway.models.mlogin import sib_login
def login():
    if 'user' in session and session['user'] != '':
        return redirect(url_for('index'))

    if request.form.get('user') == None:
        print 'error'

    return temp('login/login.html')

def user_login_out():
    sib_login.login_out()
    return redirect(url_for('login'))
