#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Set the path
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from flask.ext.script import Manager, Shell, Server
from monvelib import app

manager=Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver",Server(
    use_debugger=True,
    use_reloader=True)
)
manager.add_command("shell",Shell())

if __name__=="__main__":
    manager.run()

