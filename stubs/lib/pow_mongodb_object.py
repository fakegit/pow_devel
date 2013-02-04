import sys, datetime, os, string
import pymongo

sys.path.append(os.path.normpath("../config/"))
import powlib
import db
import pow


class PowBaseObject(object):
    """ pow base object class
        Also handles the db connection"""

    def __init__(self):
        #env = pow.global_conf["ENV"]
        self.conn = pymongo.Connection()
        if pow.conf["ENV"] == "development":
            currdb = db.development["database"]
            self.db = self.conn[currdb] 
        elif pow.conf["ENV"] == "test":
            self.db = self.conn["%s"] % db.test["database"]
        elif pow.conf["ENV"] == "production":
            self.db = self.conn["%s"] % db.production["database"]
        else:
            raise Exception("PowBaseObject.py: Unknown environment set in db.py")
        
    def get_connection(self):
        return PowBaseObject.conn
    
    def get_db(self):
        return self.db

    def get_databases(self):
        return self.conn.database_names()