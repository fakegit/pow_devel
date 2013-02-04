import os,sys
import time,datetime
import datetime
import string
import json

import pymongo

sys.path.append( os.path.abspath(os.path.join(__file__, "../lib" )))
import powlib

class PowColumn(object):
    """
        Conveniance class to be able to offer the same unser/developer 
        interface for MongoDB and SQLAlchemyself.

        Idea is to clone the Syntax of SQLAlchemy.column.
        Of course some (most) of the constraints will not be implemented 
        for MongiDB (like all SQL Types ... just doesnt matter for MongoDB)
    """
    def __init__(self, type=None, *args, **kwargs):
        self.type = type
        self.primary_key = False
        self.unique = False
        self.auto_increment = False
        if kwargs.has_key("primary_key"):
            self.primary_key = kwargs["primary_key"]
        if kwargs.has_key("unique"):
            self.unique = kwargs["unique"]
        if kwargs.has_key("auto_increment"):
            self.auto_increment = kwargs["auto_increment"]

    def a_method(self):
        pass

    def to_json(self):
        return json.dumps(self.__dict__)


