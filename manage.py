#!/usr/bin/env python

import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from rubber_ducky.src import create_app, db
from rubber_ducky.src.models import user, black_list, answer, question, reply

from rubber_ducky import user_api

app = create_app(os.getenv('FLASK_ENV'))
app.register_blueprint(user_api)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('rubber_ducky/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
