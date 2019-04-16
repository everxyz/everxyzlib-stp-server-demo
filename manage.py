#!/usr/bin/env python3
import os

from app import create_app, db
from app.models import User, File
from flask_script import Manager, Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(
        User=User,
        File=File,
        db=db
    )


manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
