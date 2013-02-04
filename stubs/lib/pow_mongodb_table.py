import os,sys
import time,datetime
import datetime
import string

import pymongo

sys.path.append( os.path.abspath(os.path.join(__file__, "../lib" )))
import powlib
from pow_mongodb_object import PowBaseObject
class PowTable(pymongo.collection.Collection):
    """
        Super Init: 
            pymongo.collection.Collection(database, name[, create=False[, **kwargs]]])
            See: http://api.mongodb.org/python/current/api/pymongo/collection.html
    """
    def __init__(self, name, create=False, **kwargs):
        """initializes the collection with the according db and connection"""
        pbo = PowBaseObject()
        super(PowTable, self).__init__(pbo.get_db(), name, create, **kwargs)

    def create_collection(self):
        self.create_table()
        return
    def create_table(self):
        self.database.createCollection(self.name)
        return

    def drop(self):
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