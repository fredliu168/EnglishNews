from flask import Flask, render_template

from . import main


@main.route('/new/<int:newid>/<string:title>/<string:source>')
def new_content(newid,title,source):
    return render_template('new-content.html', newid=newid,newTitle = title,Source=source)


@main.route('/')
def news_list():
    return render_template('news-list.html')
