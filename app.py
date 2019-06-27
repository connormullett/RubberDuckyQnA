#!/usr/bin/env python

import os

from rubber_ducky.src import create_app, db
from rubber_ducky import user_api

app = create_app(os.getenv('FLASK_ENV'))
app.register_blueprint(user_api)

app.app_context().push()

app.run()
