#!/usr/bin/env python
# encoding=utf-8
'''
task api
'''
from flask_restful import Resource
from flask import request, session
import time
import json
from runaway.models.mchangepasswd import changepasswd
class ChangePasswd(Resource):
    '''
    get item commit
    '''
    def post(self):
        postdata = request.form.get('data')
        changepasswds = changepasswd()
        res = changepasswds.update_passwd(postdata)
        return {"status": res, "message": "get commit successful!"}, 200
