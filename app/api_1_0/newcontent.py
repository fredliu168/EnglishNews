from flask import request, jsonify, current_app,send_file
import io
from . import api
import json
import requests

"""
获取新闻
"""


@api.route('/news/<int:NewsId>', methods=['GET'])
def getText(NewsId):
    url = "{}/getText.jsp?format=json&NewsId={}".format(current_app.config['SVR_NEWS_URL'], NewsId)
    r = requests.get(url)
    return r.text

"""获取新闻列表"""
@api.route('/news-list/<int:maxid>', methods=['GET'])
def getNewsList(maxid):
    url = "{}/getMyNewsList.jsp?level=0&source=0&pageCounts=20&maxId={}&format=json".format(current_app.config['SVR_NEWS_URL'], maxid)
    r = requests.get(url)
    return r.text


"""
字典查询

"""


@api.route('/query/<string:word>', methods=['GET'])
def queryWord(word):
    url = "{}{}".format(current_app.config['SVR_DIC_URL'], word)
    r = requests.get(url)
    return r.text

"""
获取新闻图片
"""
@api.route('/image/<string:imgID>', methods=['GET'])
def getImage(imgID):
    url = "{}{}".format(current_app.config['SVR_NEWS_IMG_URL'], imgID)
    r = requests.get(url)
    return send_file(io.BytesIO(r.content),
                     attachment_filename=imgID,
                     mimetype='image/png')
