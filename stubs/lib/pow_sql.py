import sys, datetime, os, getopt, shutil
import ConfigParser,string
import re

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sys.path.append( os.path.abspath(os.path.join__file__, "../lib" )))

import powlib


class PowObject(object):
    """ pow base object class"""
    __engine__= None
    __metadata__ = None
    __session__= None
    
    def dump(sql, *multiparams, **params):
        print sql.compile(dialect=engine.dialect)
    
    def __init__(self):
        dbinf = getattr(db, pow.conf["ENV"])
        PowObject.__engine__= create_engine(powlib.get_db_conn_str())
        PowObject.__metadata__ = MetaData()
        PowObject.__metadata__.bind =  PowObject.__engine__
        PowObject.__metadata__.reflect(PowObject.__engine__)
        PowObject.__session__= sessionmaker()
        PowObject.__session__.configure(bind=PowObject.__engine__)
        
        
    def getMetaData(self):
        return PowObject.__metadata__
    
    def getEngine(self):
        return PowObject.__engine__
        
    def getSession(self):
        return PowObject.__session__()
        
    def repr(self):
        return "Not implemented in class: PowObject"

class PowTable(sqlalchemy.Table):
    
    def has_many(self, tablename):
        pass
    
    def belongs_to(self, tablename):
        pass
    
    def many_to_many(self, tablename):
        pass
    
    def append_column_to_db(self, column):
        print dir(column)
        estr = "self.c." + column.name + ".create()"
        print estr
        eval( estr )
    
    def alter_column_name(self, colname, newname):
         eval("self.c." + colname + ".alter(name=\"" + newname + "\")")
         
    def create(self, **kwargs):
        col = Column('created', Text, default=datetime.datetime.now())
        self.append_column( col )
        col = Column('last_updated', Text, default=datetime.datetime.now())
        self.append_column( col )
        col = Column('id', Integer, Sequence(self.name+'_id_seq'), primary_key=True)
        self.append_column( col )
        for elem in self.columns:
            elem.name = string.lower(elem.name)
        sqlalchemy.Table.create(self, **kwargs)
        
    def drop(self, **kwargs):
        sqlalchemy.Table.drop(self, **kwargs)