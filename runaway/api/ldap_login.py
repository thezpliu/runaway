#!/usr/bin/env python
# encoding=utf-8
'''
ldap login check api
'''
from flask_restful import Resource
from flask import request
from runaway.models.mlogin import sib_login
import json

class LoginCheck(Resource):
    def post(self):

        postdata = request.get_data()
	postdata = json.loads(postdata)
	print "api form:",postdata
        if 'user' not in postdata or postdata['user'] == '':
            return {"status": 0, "message": 'User name is empty!'}, 200

        if 'password' not in postdata or postdata['password'] == '':
            return {"status": 0, "message": 'Password is empty!'}, 200

        r, u = sib_login.check_user_pass(postdata['user'], postdata['password'])

        print r, u
        if r:
            return {"status": 1, "message": 'OK'}, 200

        return {"status": 0, "message": 'Username or password error!'}, 200
