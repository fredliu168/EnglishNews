# -*- coding: UTF-8 -*-
from flask import request, jsonify, current_app, send_file
import io
from . import api
import json
import requests
import redis

"""
获取新闻
新增redis 内存数据库支持
"""


@api.route('/news/<int:NewsId>', methods=['GET'])
def getText(NewsId):
    rs = redis_cls()  # 连接resdis

    if rs is not None:
        news = rs.get(NewsId)  # 获取新闻的解释
        if news is not None:
            rs.expire(NewsId, 216000)  # 更新过期时间

            return news

    # 从网络获取新闻
    url = "{}/getText.jsp?format=json&NewsId={}".format(current_app.config['SVR_NEWS_URL'], NewsId)
    reponse = requests.get(url)
    if rs is not None:
        rs.set(NewsId, reponse.text, ex=216000)  # 设置过期时间 1小时

    return reponse.text


"""获取新闻列表"""


@api.route('/news-list/<int:maxid>', methods=['GET'])
def getNewsList(maxid):
    rs = redis_cls()  # 连接resdis

    if rs is not None:
        newslist = rs.get('maxid_{}'.format(maxid))  # 获取新闻列表
        if newslist is not None:
            return newslist

    # 从网络获获取新闻列表
    url = "{}/getMyNewsList.jsp?level=0&source=0&pageCounts=20&maxId={}&format=json".format(
        current_app.config['SVR_NEWS_URL'], maxid)
    reponse = requests.get(url)

    if rs is not None:
        rs.set('maxid_{}'.format(maxid), reponse.text, ex=108000)  # 设置过期时间 半小时

    return reponse.text


"""
字典查询

"""


@api.route('/query/<string:word>', methods=['GET'])
def queryWord(word):
    rs = redis_cls()  # 连接resdis

    if rs is not None:
        explain = rs.get(word)  # 获取单词的解释
        if explain is not None:
            rs.expire(word, 216000)  # 更新过期时间
            print('redis')
            return explain

    # 从网络获取单词解释
    url = "{}{}".format(current_app.config['SVR_DIC_URL'], word)
    reponse = requests.get(url)

    if rs is not None:
        rs.set(word, reponse.text, ex=216000)  # 设置过期时间 1小时

    return reponse.text


"""
获取新闻图片
"""


@api.route('/image/<string:imgID>', methods=['GET'])
def getImage(imgID):
    rs = redis_cls()  # 连接resdis

    if rs is not None:
        img = rs.get(imgID)  # 获取单词的解释
        if img is not None:
            rs.expire(imgID, 216000)  # 更新过期时间

            return send_file(io.BytesIO(img),
                             attachment_filename=imgID,
                             mimetype='image/png')

    url = "{}{}".format(current_app.config['SVR_NEWS_IMG_URL'], imgID)
    r = requests.get(url)

    if rs is not None:
        rs.set(imgID, r.content, ex=216000)  # 设置过期时间 1小时

    return send_file(io.BytesIO(r.content),
                     attachment_filename=imgID,
                     mimetype='image/png')


# assuming rs is your redis connection
def redis_cls():
    # ... get redis connection here, or pass it in. up to you.
    pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'], db=0)

    rs = redis.Redis(connection_pool=pool)

    try:
        rs.get(None)  # getting None returns None or throws an exception
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return None
    return rs
