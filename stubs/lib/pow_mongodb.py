import os,sys
import time,datetime
import datetime
import string
import json

import pymongo

sys.path.append( os.path.abspath(os.path.join(__file__, "../lib" )))
sys.path.append( os.path.abspath(os.path.join(__file__,"../config/")))
import powlib
import pow
import db

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


class PowBaseObject(object):
    """ pow base object class
        Also handles the db connection"""

    def __init__(self):
        #env = pow.global_conf["ENV"]
        self.conn = pymongo.Connection()
        if pow.conf["ENV"] == "development":
            currdb = db.development["database"]
            if currdb in self.conn.database_names():
                self.db = self.conn[currdb] 
            else:
                msg = "PowBaseObject.py: Database: %s does not exist. " % (currdb)
                raise Exception(msg) 
        elif pow.conf["ENV"] == "test":
            if currdb in self.conn.database_names():
                self.db = self.conn["%s"] % db.test["database"]
            else:
                msg = "PowBaseObject.py: Database: %s does not exist. " % (currdb)
                raise Exception(msg)
        elif pow.conf["ENV"] == "production":
            if currdb in self.conn.database_names():  
                self.db = self.conn["%s"] % db.production["database"]
            else:
                msg = "PowBaseObject.py: Database: %s does not exist. " % (currdb)
                raise Exception(msg)
        else:
            raise Exception("PowBaseObject.py: Unknown environment set in db.py")
        
    def get_connection(self):
        return PowBaseObject.conn
    
    def get_db(self):
        return self.db

    def get_databases(self):
        return self.conn.database_names()

class PowTable(pymongo.collection.Collection):
    """
        Super Init: 
            pymongo.collection.Collection(database, name[, create=False[, **kwargs]]])
            See: http://api.mongodb.org/python/current/api/pymongo/collection.html
    """
    def __init__(self, name, schema, create=False, **kwargs):
        """initializes the collection with the according db and connection"""
        pbo = PowBaseObject()
        super(PowTable, self).__init__(pbo.get_db(), name, create, **kwargs)
        self.schema = schema

    def create_collection(self):
        """ creates a collection in mongoDB 
            This is not explicitly neccessary, though"""
        self.create_table()
        return

    def create_table(self):
        """ creates a collection in mongoDB 
            This is not explicitly neccessary, though"""
        self.database.createCollection(self.name)
        return

    def drop(self):
        """ drops the collection"""
        self.drop()

    def has_many(self, tablename):
        pass
    
    def belongs_to(self, tablename):
        pass
    
    def many_to_many(self, tablename):
        pass
    
    def append_column_to_db(self, column):
        pass
    
    def alter_column_name(self, colname, newname):
         pass