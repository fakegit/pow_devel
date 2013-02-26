#
# initializes the default_environment for PoW on mongoDB
# especially the app and schema_versions collections
#
# khz 31/01/2013

import sys
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))
import string
import powlib
import pymongo

if __name__ == "__main__":
    print "make sure you have mongoDB installed and started"
    print "make sure you have setup the right db-names"
    print "---------------------------------------------------"
    var = raw_input( "please confirm with (y)es or (q)uit !" )
    
    if var == "q" or var =="Q":
        sys.exit(0)
    
    appname = string.lower("test")

    print "initializing the Pow base collections...."

    schema_versions = {
        "version"       :   "0",
        "comment"       :   "initial", 
        "filename"      :   "NONE",
        "last_updated"  :   datetime.datetime,
        "schema"        :   None

    }
    
    app = {
        "name"          :   appname, 
        "filename"      :   "NONE",
        "last_updated"  :   datetime.datetime
    }
     
    self.conn = pymongo.Connection()
    db = self.conn["%s_pow"] % appname
    
    db.schema_versions.save(schema_version)
    db.app_info.save(app)
    print "done! "
    