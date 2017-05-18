# -*- coding: UTF-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SVR_NEWS_URL = 'https://cms.iyuba.com/cmsApi/' #新闻的地址
    SVR_DIC_URL= 'https://fanyi.youdao.com/openapi.do?keyfrom=f2ec-org&key=1787962561&type=data&doctype=json&version=1.1&q=' #有道翻译
    SVR_NEWS_IMG_URL = 'http://static.iyuba.com/cms/news/image/' #新闻图片

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'default': DevelopmentConfig

}
