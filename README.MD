
基于Pyton Flask 框架的H5页面,
英语新闻轻松读,点击单词自动查询有道字典

演示地址:https://englishnews.herokuapp.com/

发布步骤:

git add -A
git commit -m  "备注"
git push origin master
heroku logs --tail

manage的使用

manage.py replaces running the app with python app.py. It is provided by Flask-Script, not Flask-Migrate which just adds commands to it. Use the runserver command it supplies to run the dev server. You can pass the host and port to that command:

```py
python manage.py runserver -h localhost -p 8080 -d
```

or you can override the defaults when configuring the manager:

```py
manager = Manager()

manager.add_command('runserver', Server(host='localhost', port=8080, debug=True)

```

执行docker

```
docker run -v $PWD:/usr/www/app -w /usr/www/app -p 5000:5000 english_news python manage.py runserver -h 0.0.0.0
```

安装 uWSGI
```
(venv)my_flask root$ pip install uwsgi
```

使用uwsgi时一直运行未成功,卸载重装也不行,后面在manage.py加上下列函数就可以了:
 @manager.command def deploy():     """Run deployment tasks."""     pass


获取图片的时候出现错误
```
SystemError: <built-in function uwsgi_sendfile> returned a result with an error set
```
查找时看到解决方案:

https://github.com/unbit/uwsgi/issues/1126
Just got this with Python 3.6.1 and flask send_file(), running uwsgi 2.0.15 with --wsgi-disable-file-wrapper makes the problem go away.
运行:

```
uwsgi config.ini --wsgi-disable-file-wrapper
```
