#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from momeet.app import create_app, db

manager = Manager(create_app)

if __name__ == '__main__':
    migrate = Migrate(manager.app(), db)
    manager.add_command('db', MigrateCommand)
    manager.run()
