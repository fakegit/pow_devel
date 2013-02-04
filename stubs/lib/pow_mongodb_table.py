import os,sys
import time,datetime
import datetime
import string

import pymongo

sys.path.append( os.path.abspath(os.path.join__file__, "../lib" )))
import powlib

class PowTable(pymongo.collection):
    
    """
        Super Iinit: 
            pymongo.collection.Collection(database, name[, create=False[, **kwargs]]])
            See: http://api.mongodb.org/python/current/api/pymongo/collection.html
    """
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
         
    def create_collection(self):
        self.create_table()
        return
    def create_table(self):
        self.database.createCollection(self.name)
        return

    def drop(self):
        self.drop()