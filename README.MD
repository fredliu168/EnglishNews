
# 基于Pyton Flask 框架的H5页面,站点部署到阿里云

英语新闻轻松读,点击单词自动查询有道字典

演示地址:
```
https://www.qzcool.com/
```

进入虚拟环境

```
source /home/www/eglish_venv/bin/activate
```

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
```
git add -A
git commit -m  "备注"
git push origin master
heroku logs --tail
```
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

### 安装 uWSGI

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

### 阿里云部署

mac 远程连接阿里云服务器

```
ssh root@IPaddress
```

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

Supervisor|[http://supervisord.org/configuration.html]可以同时启动多个应用，最重要的是，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。

```
sudo apt-get install supervisor
```

Supervisor 的全局的配置文件位置在：

```
/etc/supervisor/supervisor.conf
```

正常情况下我们并不需要去对其作出任何的改动，只需要添加一个新的 *.conf 文件放在
```
/etc/supervisor/conf.d/
```
下就可以，那么我们就新建立一个用于启动 my_flask 项目的 uwsgi 的 supervisor 配置 (命名为：englishnews_supervisor.conf)：

```
/etc/supervisor/conf.d/englishnews_supervisor.conf
```

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


处理URL特殊字符问题

```
  <script type="text/javascript">
        function URLencode(sStr) {//处理url中特殊保留字符?
            return encodeURI(sStr).replace(/\?/g, '%3F').replace(/\+/g, '%2B').replace(/\"/g, '%22').replace(/\'/g, '%27').replace(/\//g, '%2F');
        }
  </script>
```

### nginx 配置

配置路径
```
cd /etc/nginx/sites-available
```
日志目录
```
access_log /var/log/nginx/access.log;

error_log /var/log/nginx/error.log;

```
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

```
service nginx restart
```

# Let's Encrypt，免费好用的 HTTPS 证书, 配置步骤

### 创建帐号

首先创建一个目录，例如 ssl，用来存放各种临时文件和最后的证书文件。

本项目放在

```
/home/www/ssl
```

进入这个目录，创建一个 RSA 私钥用于 Let's Encrypt 识别你的身份：

```

openssl genrsa 4096 > account.key

```

### 创建 CSR 文件

接着就可以生成 CSR（Certificate Signing Request，证书签名请求）文件了。在这之前，还需要创建域名私钥（一定不要使用上面的账户私钥），根据证书不同类型，域名私钥也可以选择 RSA 和 ECC 两种不同类型。以下两种方式请根据实际情况二选一。

1）创建 RSA 私钥（兼容性好）：

```
openssl genrsa 4096 > domain.key
```

有了私钥文件，就可以生成 CSR 文件了。在 CSR 中推荐至少把域名带 www 和不带 www 的两种情况都加进去，其它子域可以根据需要添加（目前一张证书最多可以包含 100 个域名）：

配置https

```
openssl req -new -sha256 -key domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:qzcool.com,DNS:www.qzcool.com")) > domain.csr
```

### 配置验证服务
我们知道，CA 在签发 DV（Domain Validation）证书时，需要验证域名所有权。传统 CA 的验证方式一般是往 admin@yoursite.com 发验证邮件，而 Let's Encrypt 是在你的服务器上生成一个随机验证文件，再通过创建 CSR 时指定的域名访问，如果可以访问则表明你对这个域名有控制权。
首先创建用于存放验证文件的目录，例如：

```
mkdir /home/www/challenges/
```

然后配置一个 HTTP 服务，以 Nginx 为例：

```
server {
    server_name www.qzcool.com;

    location ^~ /.well-known/acme-challenge/ {
        alias /home/www/challenges/;
        try_files $uri =404;
    }

    location / {
        rewrite ^/(.*)$ https://www.qzcool.com/$1 permanent;
    }
}

```

以上配置优先查找 /home/www/challenges/ 目录下的文件，如果找不到就重定向到 HTTPS 地址。这个验证服务以后更新证书还要用到，建议一直保留。

### 获取网站证书

先把 acme-tiny 脚本保存到之前的 ssl 目录：

```
wget https://raw.githubusercontent.com/diafygi/acme-tiny/master/acme_tiny.py
```

指定账户私钥、CSR 以及验证目录，执行脚本：

```
python acme_tiny.py --account-key account.key --csr domain.csr --acme-dir /home/www/challenges/ > signed.crt
```


如果一切正常，当前目录下就会生成一个 signed.crt，这就是申请好的证书文件。

搞定网站证书后，还要下载 Let's Encrypt 的中间证书。我在之前的文章中讲过，配置 HTTPS 证书时既不要漏掉中间证书，也不要包含根证书。在 Nginx 配置中，需要把中间证书和网站证书合在一起：

```
wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > intermediate.pem
cat signed.crt intermediate.pem > chained.pem
```

为了后续能顺利启用 OCSP Stapling，我们再把根证书和中间证书合在一起：

```
wget -O - https://letsencrypt.org/certs/isrgrootx1.pem > root.pem
cat intermediate.pem root.pem > full_chained.pem
```
最终，修改 Nginx 中有关证书的配置并 reload 服务即可：

```
ssl_certificate     /home/www/ssl/chained.pem;
ssl_certificate_key /home/www/ssl/domain.key;
```

下面是nginx 完整配置


```
server {
    listen  443 ssl http2 fastopen=3 reuseport;

    # 如果你使用了 Cloudflare 的 HTTP/2 + SPDY 补丁，记得加上 spdy
    # listen               443 ssl http2 spdy fastopen=3 reuseport;

    server_name          www.qzcool.com;
    server_tokens        off;


    # 中间证书 + 站点证书
    ssl_certificate      /home/www/ssl/chained.pem;

    # 创建 CSR 文件时用的密钥
    ssl_certificate_key  /home/www/ssl/domain.key;


    # https://github.com/cloudflare/sslconfig/blob/master/conf
    ssl_ciphers                EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;

    ssl_prefer_server_ciphers  on;

    ssl_protocols              TLSv1 TLSv1.1 TLSv1.2;

    ssl_session_cache          shared:SSL:50m;
    ssl_session_timeout        1d;

    ssl_session_tickets        on;

    ssl_stapling               on;
    ssl_stapling_verify        on;

    # 根证书 + 中间证书
    # https://imququ.com/post/why-can-not-turn-on-ocsp-stapling.html
    ssl_trusted_certificate    /home/www/ssl/full_chained.pem;

      location / {
      proxy_pass  http://127.0.0.1:5000/;
      proxy_set_header    Host    $host;
      proxy_set_header    X-Real-IP   $remote_addr;
      }
    }

server {
    server_name www.qzcool.com;

    location ^~ /.well-known/acme-challenge/ {
        alias /home/www/challenges/;
        try_files $uri =404;
    }

    location / {
        rewrite ^/(.*)$ https://www.qzcool.com/$1 permanent;
    }
}
```
### 配置自动更新

Let's Encrypt 签发的证书只有 90 天有效期，推荐使用脚本定期更新。例如我就创建了一个 renew_cert.sh 并通过 chmod a+x renew_cert.sh 赋予执行权限。文件内容如下：

```
#!/bin/bash

cd /home/www/ssl/
python acme_tiny.py --account-key account.key --csr domain.csr --acme-dir /home/www/challenges/ > signed.crt || exit
wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > intermediate.pem
cat signed.crt intermediate.pem > chained.pem
service nginx reload

```

crontab 中使用绝对路径比较保险，crontab -e 加入以下内容：

```
0 0 1 * * /home/ssl/renew_cert.sh >/dev/null 2>&1

```


# Redis 访问

### mac 安装redis

通过homebrew安装
```
brew install redis
```
1 启动redis服务
执行以下命令

```
redis-server /usr/local/etc/redis.conf
```


To have launchd start redis now and restart at login:
```
  brew services start redis
```
Or, if you don't want/need a background service you can just run:
```
  redis-server /usr/local/etc/redis.conf
```

2 查看redis服务是否启动

```
ps aux | grep redis
```

通过redis-cli命令可以启动redis客户端
```
redis-cli
```

