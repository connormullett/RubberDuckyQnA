
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from rubber_ducky.src.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('rubber_ducky.src.config.Development')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'not_my_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL'))


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('rubber_ducky.src.config.Testing')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('TEST_DATABASE_URL')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('rubber_ducky.src.config.Production')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
