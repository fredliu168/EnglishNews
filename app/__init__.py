# -*- coding: UTF-8 -*-

from config import config
from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    # 页面
    from .main import main  as main_blueprint
    app.register_blueprint(main_blueprint)

    # 接口
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v2.0')

    from .api_2_0 import api as api_2_0_blueprint
    app.register_blueprint(api_2_0_blueprint, url_prefix='/api/v1.0')

    from .api_3_0 import api as api_3_0_blueprint
    app.register_blueprint(api_3_0_blueprint, url_prefix='/api/v3.0')

    return app
