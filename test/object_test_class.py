import asyncio

import peewee_async

from database import Items, database
from config import config


def get_config():
    return config


class ObjectTestClass:

    @classmethod
    def init_database(cls):
        _config = get_config()
        database.init(**_config)
        database.objects = peewee_async.Manager(database=database)

    @classmethod
    def setup_class(cls):
        cls.init_database()
        database.create_tables(models=[Items])

    @classmethod
    def teardown_class(cls):
        database.drop_tables(models=[Items])

    def setup_method(self, method):
        self.init_database()

    def teardown_method(self, method):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(database.objects.close())
        loop.close()