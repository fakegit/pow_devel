import sys,os,datetime
import os.path
import string
import logging

# the libraries

sys.path.append( os.path.normpath(os.path.join(__file__, "../../../stubs/lib" )) )

import powlib
from pow_base_object import PowBaseObject
import pdb

class BaseModel(object):
    def __init__(self):
        # This is the "base" constructor.
        pass
    
    def setup_attributes(self, klass, attrs):
        for elem in attrs:
            setattr(klass, elem, "")

    @classmethod
    def init(klass, model):
        # This is one special constructor.
        print klass
        p = klass()
        p.pbo = PowBaseObject()
        p.db = p.pbo.get_db()
        p.collection = p.db[model]    
        p.setup_attributes(p, ["title", "name"])
        return p

    def find_by_id(self, id):
        self.__dict__ = self.collection.find_one({"_id" : id})
        return 
            
    def find_one(self, query):
        return
    
    def save(self):
        self.collection.save(self.__dict__)

    def set(self, name, value):
        setattr(self.parent, name, value)
        return
    
    def get(self, name):
        return getattr(self, name)

    def update(self):
        """ updates this record """
        dt = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
        dt = urllib.unquote(dt)
        self.last_updated = dt
        self.session.merge(self)
        self.session.commit()

    def create(self):
        """ adds a new record to the db """
        dt = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
        #dt = urllib.unquote(dt)
        self.set("created", dt)
        self.set("last_updated", dt)
        self.session.merge(self)
        self.session.commit()

    def delete(self):
        """ deletes this record """
        s = sqlalchemy.sql.delete(self.__table__, self.__table__.columns.id==self.id)
        self.session.execute(s)
        self.session.commit()


    def generate_accessor_methods(self):
        #
        """generates the convenient getAttribute() and setAttribute Methods
        and sets them as accessors for this models Attributes """
        mstr = ""
        self.has_accessor_methods = True
        for item in self.parent.__table__.columns:
            #getter
            mstr = ""
            method_name = "get_"+ item.name
            setter = method_name
            tmp_meth_name = "foo"
            mstr +=     "def foo(self):" + powlib.newline
            mstr += powlib.tab + "return self." + str(item.name) + powlib.newline
            #print mstr
            exec(mstr)
            self.parent.__dict__[method_name] = types.MethodType(foo,self.parent)
            
            
            # setter
            mstr = ""
            method_name = "set_"+ item.name
            getter = method_name
            tmp_meth_name = "foo"
            mstr +=     "def foo(self, value):" + powlib.newline
            mstr += powlib.tab + "self." + str(item.name) + " = value " + powlib.newline
            #print mstr
            exec(mstr)
            self.parent.__dict__[method_name] = types.MethodType(foo,self.parent)
            
            #cmd_str = "self.__table__." + item + "=property(" + getter + "," + setter + ")"
            #eval(cmd_str)

    