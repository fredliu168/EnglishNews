from app import create_app
from flask_script import Manager

app = create_app('default')

manager = Manager(app)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, threaded=True)
