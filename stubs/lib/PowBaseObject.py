import sys, datetime, os, getopt, shutil
import ConfigParser,string
import re

import pymongo
from bson import ObjectID

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
            db = self.conn["%s"] % db.development["database"]
        elif pow.conf["ENV"] == "test":
            db = self.conn["%s"] % db.test["database"]
        elif pow.conf["ENV"] == "production":
            db = self.conn["%s"] % db.production["database"]
        else:
            raise Exception("PowBaseObject.py: Unknown environment set in db.py")
        
    def get_connection(self):
        return PowBaseObject.conn
    
    def get_databases(self):
        return self.conn.database_names()