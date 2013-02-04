import os,sys
import time,datetime


sys.path.append( os.path.abspath(os.path.join__file__, "../lib" )))
import powlib
from pow_base_object import PowObject

class BaseMigration(PowObject):
    
    def __init__(self, table = None):
        PowObject.__init__(self)
        self.table = table
            
    def create_table(self, table = None):
        if self.table:
            self.table.create(bind=PowObject.__engine__, checkfirst=True)
        else:
            raise StandardError("Pow ERROR: table was None")
        
    def drop_table(self, model = None):
        try:
            if model == None:
                self.table = Table(self.table_name, PowObject.__metadata__, autoload = True )
            else:
                self.table = model.__table__
            if self.table != None:
                self.table.drop(bind=PowObject.__engine__, checkfirst=True)
        except:
            raise StandardError("Pow ERROR: table does not exist")