# -*- coding: UTF-8 -*-
from flask import request, jsonify, current_app, send_file
import io
from . import api
import json
import requests
import redis
import hashlib
import random

"""
获取新闻
新增redis 内存数据库支持
"""


@api.route('/news/<int:NewsId>', methods=['GET'])
def getText(NewsId):

    REDIS_NEWS_TIME = current_app.config['REDIS_NEWS_TIME']
    rs = redis_cls()  # 连接resdis

    if rs is not None:
        news = rs.get(NewsId)  # 获取新闻的解释
        if news is not None :
            rs.expire(NewsId, REDIS_NEWS_TIME)  # 更新过期时间

            return news

    # 从网络获取新闻
    url = "{}/getText.jsp?format=json&NewsId={}".format(current_app.config['SVR_NEWS_URL'], NewsId)
    reponse = requests.get(url)

    print(reponse.status_code)

    if rs is not None and reponse.status_code == 200:
        rs.set(NewsId, reponse.text, ex=REDIS_NEWS_TIME)  # 设置过期时间 1小时

    print(reponse.text)

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

    if rs is not None and reponse.status_code == 200:
        REDIS_NEWS_LIST_TIME = current_app.config['REDIS_NEWS_LIST_TIME']
        rs.set('maxid_{}'.format(maxid), reponse.text, ex=REDIS_NEWS_LIST_TIME)  # 设置过期时间 半小时

    return reponse.text


"""
字典查询

"""


@api.route('/query/<string:word>', methods=['GET'])
def queryWord(word):
    REDIS_WORD_TIME = current_app.config['REDIS_WORD_TIME']
    rs = redis_cls()  # 连接resdis

    if rs is not None:
        explain = rs.get(word)  # 获取单词的解释
        if explain is not None:
            rs.expire(word, REDIS_WORD_TIME)  # 更新过期时间

            return explain

    #sign	text	签名，通过md5(appKey+q+salt+密钥)生成	True	appKey+q+salt+密钥的MD5值 5GFv0iwSAjnprcfKoktX9CNtxK2z79sj
    appKey = '2284dabba457327d'
    secretkey = '5GFv0iwSAjnprcfKoktX9CNtxK2z79sj'
    q = word
    salt ='{}'.format(random.randint(1, 200))
    sign = MD5(appKey+q+salt+secretkey)

    url = 'https://openapi.youdao.com/api?q={q}&from=en&to=zh_CHS&appKey={appKey}&salt={salt}&sign={sign}'.format(q=q,appKey=appKey,salt=salt,sign=sign)

    print(url)
    # 从网络获取单词解释
    #url = "{}{}".format(current_app.config['SVR_DIC_URL'], word)

    reponse = requests.get(url)

    #print(reponse.text)
    if rs is not None and reponse.status_code == 200:
        #json_str = json.dumps(reponse.text)
        #print(json_str)
        rs.set(word, reponse.text, ex=REDIS_WORD_TIME)  # 设置过期时间 1小时

    #print(reponse.text)
    return reponse.text


"""
获取新闻图片
"""


@api.route('/image/<string:imgID>', methods=['GET'])
def getImage(imgID):
    rs = redis_cls()  # 连接resdis
    REDIS_IMG_TIME = current_app.config['REDIS_IMG_TIME']

    if rs is not None:
        img = rs.get(imgID)  # 获取单词的解释
        if img is not None:
            rs.expire(imgID, REDIS_IMG_TIME)  # 更新过期时间

            return send_file(io.BytesIO(img),
                             attachment_filename=imgID,
                             mimetype='image/png')

    url = "{}{}".format(current_app.config['SVR_NEWS_IMG_URL'], imgID)
    r = requests.get(url)


    if rs is not None and r.status_code == 200:
        rs.set(imgID, r.content, ex=REDIS_IMG_TIME)  # 设置过期时间 1小时

    return send_file(io.BytesIO(r.content),
                     attachment_filename=imgID,
                     mimetype='image/png')


def MD5(src):
    # md5 加密
    md5 = hashlib.md5()
    md5.update(src.encode('utf-8'))
    return md5.hexdigest()

# assuming rs is your redis connection
def redis_cls():
    # ... get redis connection here, or pass it in. up to you.
    pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'], db=0)

    rs = redis.Redis(connection_pool=pool)

    try:
        rs.get(None)  # getting None returns None or throws an exception
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        print("redis.exceptions.ConnectionError")
        return None
    return rs
