
import os

from rubber_ducky.src import create_app, db
from rubber_ducky import user_api

application = create_app(os.getenv('FLASK_ENV'))
application.register_blueprint(user_api)

application.app_context().push()

application.run()

