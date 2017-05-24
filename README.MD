
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