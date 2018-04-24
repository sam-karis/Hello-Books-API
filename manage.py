import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db, models

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
