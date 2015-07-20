from flask.ext.script import Manager, Shell
from flask.ext.migrate import MigrateCommand

from ton import app


# init manager and add migration commands
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
