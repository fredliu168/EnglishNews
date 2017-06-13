from app import create_app
from flask_script import Manager, Shell
import os

app = create_app('default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))



@manager.command
def deploy():
    """Run deployment tasks."""
    pass


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # app.run('0.0.0.0', port=port, threaded=True)
    # app.run()
    manager.run()
