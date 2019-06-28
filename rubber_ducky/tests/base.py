
from flask_testing import TestCase
from rubber_ducky.src import db
from manage import app


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('rubber_ducky.src.config.TestingConfig')
        return app
    
    def setUp(self):
        db.create_all()
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
