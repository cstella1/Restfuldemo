from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps.user.model import User
from apps import create_app
from exts import db

app = create_app()

manager = Manager(app=app)

migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def hell_world():
    return 'HELLO'


if __name__ == '__main__':
    manager.run()
