
基于Pyton Flask 框架的H5页面,
英语新闻轻松读,点击单词自动查询有道字典

演示地址:http://www.qzcool.com/

生成需求文件
```
(venv)$ pip freeze >requirement.txt
```
安装

```
(venv)$ pip install -r requirement.txt
```

拉取最新代码

```
git pull eng master
```

覆盖本地文件

```
git reset --hard

git pull

```


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


mac 远程连接阿里云服务器

ssh root@IPaddress

安装虚拟环境

```
pyvenv /home/www/venv_english

```

激活虚拟环境

```
source venv_english/bin/acitvate
```

启动应用

```
python manage.py runserver -h 0.0.0.0
```
或者
```
uwsgi config.ini --wsgi-disable-file-wrapper
```

### 安装 Supervisor

[Supervisor|http://supervisord.org/configuration.html]可以同时启动多个应用，最重要的是，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。

sudo apt-get install supervisor
Supervisor 的全局的配置文件位置在：

/etc/supervisor/supervisor.conf

正常情况下我们并不需要去对其作出任何的改动，只需要添加一个新的 *.conf 文件放在

/etc/supervisor/conf.d/

下就可以，那么我们就新建立一个用于启动 my_flask 项目的 uwsgi 的 supervisor 配置 (命名为：englishnews_supervisor.conf)：


/etc/supervisor/conf.d/englishnews_supervisor.conf

```
[program:englishnews]
# 启动命令入口
command=/home/www/venv_english/bin/uwsgi /home/www/EnglishNews/config.ini

# 命令程序所在目录
directory=/home/www/EnglishNews
#运行命令的用户名
user=root

autostart=true
autorestart=true
#日志地址
stdout_logfile=/home/www/EnglishNews/logs/uwsgi_supervisor.log
stderr_logfile=/home/www/EnglishNews/logs/err.log
stopsignal=INT
[supervisord]
```

启动服务
```
sudo service supervisor start
```
终止服务
```
sudo service supervisor stop
```

### nginx 配置

配置路径

cd /etc/nginx/sites-available

```
server {
      listen  80;
      server_name www.qzcool.com; #公网地址

      location / {
      proxy_pass  http://127.0.0.1:5000/;
      proxy_set_header    Host    $host;
      proxy_set_header    X-Real-IP   $remote_addr;
      }
    }
```

重新启动nginx

service nginx restart