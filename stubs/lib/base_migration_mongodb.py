import os,sys
import time,datetime


sys.path.append( os.path.abspath(os.path.join__file__, "../lib" )))
import powlib
from pow_mongodb import PowObject

class BaseMigration(PowObject):
    
    def __init__(self, table = None):
        PowObject.__init__(self)
        self.table = table
            
    def create_table(self, table = None):
        try:
            self.table.create_table()
        except:
            raise StandardError("Pow ERROR: collection could not be created")
        
    def drop_table(self, model = None):
        try:
            self.table.drop_table()
        except:
            raise StandardError("Pow ERROR: collection could not be dropped")