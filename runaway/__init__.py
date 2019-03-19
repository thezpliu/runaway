# coding=utf-8
'''
程序入口文件
'''
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from runaway.config.urls import regist_urls


template_folder = 'template'

app = Flask(__name__, template_folder=template_folder)

app.secret_key = 'runaway'
#'mELM9rRYYAmZ6N5jiLS5kVG6'

app.permanent_session_lifetime = timedelta(days=7)  # 7天过期

runaway_api = Api(app)

regist_urls(app, runaway_api)  # 注册url路由
