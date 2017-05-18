from app import create_app
from flask_script import Manager
import os
app = create_app('default')

manager = Manager(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port, threaded=True)
