# -*- coding: UTF-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SVR_NEWS_URL = 'http://cms.iyuba.com/cmsApi/' #新闻的地址
    SVR_DIC_URL= 'http://fanyi.youdao.com/openapi.do?keyfrom=f2ec-org&key=1787962561&type=data&doctype=json&version=1.1&q=' #有道翻译
    SVR_NEWS_IMG_URL = 'http://static.iyuba.com/cms/news/image/' #新闻图片
    REDIS_PORT = '6379' # redis 连接 端口
    REDIS_HOST = 'localhost'
    REDIS_WORD_TIME = 604800 # 单词保持时间 一星期
    REDIS_NEWS_TIME = 604800  # 新闻保持时间 一星期
    REDIS_NEWS_LIST_TIME = 3600 # 新闻列表 1小时
    REDIS_IMG_TIME = 604800 # 图片保持时间 一星期
    YOUDAO_API= 'https://openapi.youdao.com/api' # 有道翻译api
    YOUDAO_APPID = '2284dabba457327d'
    YOUDAO_KEY = '5GFv0iwSAjnprcfKoktX9CNtxK2z79sj'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'default': DevelopmentConfig

}
