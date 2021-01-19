# -*- coding: utf-8 -*-

"""
Models to store scraped data in a database.
"""

import inspect

from peewee import Model
from playhouse.db_url import connect
from peewee import CompositeKey, IntegerField, TextField
import os

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = DATABASE

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delitem__(self, key):
        return setattr(self, key, None)

    @classmethod
    def primary_keys(cls):
        pk = cls._meta.primary_key
        if "field_names" in pk.__dict__:
            names = pk.field_names
        else:
            names = (pk.name,)
        return names

    @classmethod
    def from_scrapy_item(cls, item):
        query = cls.insert(**item).on_conflict("REPLACE")
        return query.execute()


# ----------------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------------


class Locality(BaseModel):
    entidad = TextField()
    municipio = TextField()
    confirmados = IntegerField()
    defunciones = IntegerField()
    activos = IntegerField()
    ambulatorios = IntegerField()
    ambulatorios_fallecidos = IntegerField()
    hospitalizados = IntegerField()
    hospitalizados_fallecidos = IntegerField()
    intubados = IntegerField()
    intubados_fallecidos = IntegerField

    class Meta:
        db_table = "localities"
        indexes = [(("entidad", "municipio"), True)]
        primary_key = CompositeKey("entidad", "municipio")


class Daily(BaseModel):
    casos = TextField()
    defunciones = TextField()
    fecha = TextField()

    class Meta:
        db_table = "daily"


# ----------------------------------------------------------------------------
# Automatically create the tables...
# ----------------------------------------------------------------------------


def create_tables():
    models = []
    for name, cls in globals().items():
        if inspect.isclass(cls) and issubclass(cls, BaseModel):
            if name == "BaseModel":
                continue
            models.append(cls)
    DATABASE.create_tables(models, safe=True)


if __name__ == "__main__":
    create_tables()
