# coding=utf-8
# Copyright 2018-2020 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from sqlalchemy import Column, Integer
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database

from src.catalog.sql_config import SQLConfig
from src.utils.logging_manager import LoggingLevel
from src.utils.logging_manager import LoggingManager

db_session = SQLConfig().session


class CustomModel:
    """This overrides the default `_declarative_constructor` constructor.

    It skips the attributes that are not present for the model, thus if a
    dict is passed with some unknown attributes for the model on creation,
    it won't complain for `unkwnown field`s.
    Declares and int id field for all tables
    """
    query = db_session.query_property()
    _id = Column('id', Integer, primary_key=True)

    def __init__(self, **kwargs):
        cls_ = type(self)
        for k in kwargs:
            if hasattr(cls_, k):
                setattr(self, k, kwargs[k])
            else:
                continue

    def save(self):
        """Add and commit

        Returns: saved object

        """
        try:
            db_session.add(self)
            self._commit()
        except Exception as e:
            LoggingManager().log("Object already exists in database",
                                 LoggingLevel.ERROR)
            raise e
        return self

    def update(self, **kwargs):
        """Update and commit

        Args:
            **kwargs: attributes to update

        Returns: updated object

        """
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        return self.save()

    def delete(self):
        """Delete and commit"""
        try:
            db_session.delete(self)
            self._commit()
        except Exception:
            LoggingManager().log("Object couldn't be deleted",
                                 LoggingLevel.ERROR)
            raise Exception

    def _commit(self):
        """Try to commit. If an error is raised, the session is rollbacked."""
        try:
            db_session.commit()
        except DatabaseError:
            db_session.rollback()
            LoggingManager().log(
                "Exception occurred while committing to database.",
                LoggingLevel.ERROR)
            raise Exception("Exception occurred while committing to database.")


# Custom Base Model to be inherited by all models
BaseModel = declarative_base(
    cls=CustomModel,
    constructor=None,
    bind=SQLConfig().engine)


def init_db():
    """Create database if doesn't exist and create all tables."""
    engine = SQLConfig().engine
    if not database_exists(engine.url):
        LoggingManager().log("Database does not exist, creating database.",
                             LoggingLevel.INFO)
        create_database(engine.url)
    LoggingManager().log("Creating tables", LoggingLevel.INFO)
    BaseModel.metadata.create_all()


def drop_db():
    """Drop all of the record from tables and the tables themselves. Drop the
    database as well."""
    engine = SQLConfig().engine
    if database_exists(engine.url):
        db_session.commit()
        BaseModel.metadata.drop_all()
        drop_database(engine.url)
