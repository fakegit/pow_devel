#
# Author:       khz
# Date created: 17/10/2006
# purpose:      POW lib
# Changes:
# 17/10/2006    initially created
#
import sys, datetime, os, getopt, shutil
import ConfigParser,string
import re

from sqlalchemy import MetaData
from sqlalchemy import create_engine

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../config" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../controllers" )) )
import pow
import db

hidden_list = ["created", "last_updated", "group", "user", "id", "password"]
linesep = "\n"
newline = linesep
tab = "    "
MAX_SYSOUT = 50
PARTS_DIR = "./stubs/partials/"
#
# (pattern, search, replace) regex english plural rules tuple
# taken from : http://www.daniweb.com/software-development/python/threads/70647
rule_tuple = (
    ('[ml]ouse$', '([ml])ouse$', '\\1ice'),
    ('child$', 'child$', 'children'),
    ('booth$', 'booth$', 'booths'),
    ('foot$', 'foot$', 'feet'),
    ('ooth$', 'ooth$', 'eeth'),
    ('l[eo]af$', 'l([eo])af$', 'l\\1aves'),
    ('sis$', 'sis$', 'ses'),
    ('man$', 'man$', 'men'),
    ('ife$', 'ife$', 'ives'),
    ('eau$', 'eau$', 'eaux'),
    ('lf$', 'lf$', 'lves'),
    ('[sxz]$', '$', 'es'),
    ('[^aeioudgkprt]h$', '$', 'es'),
    ('(qu|[^aeiou])y$', 'y$', 'ies'),
    ('$', '$', 's')
    )

def uc(instr):
    #encoding = readconfig("pow.cfg","global","DEFAULT_ENCODING")
    encoding = pow.global_conf["DEFAULT_ENCODING"]
    return unicode(instr, encoding)
    
def regex_rules(rules=rule_tuple):
    # also to pluralize
    for line in rules:
        pattern, search, replace = line
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)

# the following three functions are taken from:
# http://c2.com/cgi/wiki?MixinsForPython 
# will use them to test mixin of plugin functionalities into models and controllers.
# also see comment to mixin function related to the controvery of mixin vs multiple inheritance.
def mixInClass (base, addition):

    """Mixes in place, i.e. the base class is modified.
    Tags the class with a list of names of mixed members.
    """
    assert not hasattr(base, '_mixed_')
    mixed = []
    for item, val in addition.__dict__.items():
        if not hasattr(base, item):
            setattr(base, item, val)
            mixed.append (item)
    base._mixed_ = mixed



def unMixClass (cla):

    """Undoes the effect of a mixin on a class. Removes all attributes that
    were mixed in -- so even if they have been redefined, they will be
    removed.
    """
    for m in cla._mixed_: #_mixed_ must exist, or there was no mixin
        delattr(cla, m)
    del cla._mixed_



def mixedInClass (base, addition):

    """Same as mixInClass, but returns a new class instead of modifying
    the base.
    """
    class newClass: pass
    newClass.__dict__ = base.__dict__.copy()
    mixIn (newClass, addition)
    return newClass
def mixin(*args):
    """Decorator for mixing in mixins ;) 
        I nkow that there is a BIG debate about mixins vs. multiple inheritance.
        I will try both but personally do not like to have many multi inheritances per class.
           IMO looks ugly. if multi inheritances are also stacked it gets quite copmplex to follow.
        taken from: http://stackoverflow.com/questions/4139508/in-python-can-one-implement-mixin-behavior-without-using-inheritance
        Adapted so that methods already in the Class will not be overwritten.
        Could be chamged semantically to overwrite in the future but then will need to 
        make sure that _meth and __methods are still kept original.
    """
    def inner(cls):
        for a,k in ((a,k) for a in args for k,v in vars(a).items() if callable(v)):
            #print a, type(a)
            #print k, type(k)
            if hasattr(cls, k): 
                print 'method name conflict %s' % (str(k))
            else:
                setattr(cls, k, getattr(a, k))
        return cls
    return inner

def replace_string_in_file( absfilename, origstr, repstr):
    # set correct Appname in pow_router.wsgi
    f = open(os.path.join(absfilename), "r")
    instr = f.read()
    instr = instr.replace(origstr, repstr)
    f.close()
    f = open(os.path.join(absfilename), "w")
    f.write(instr)
    f.close()
    return
    
def plural(noun):
    # the final pluralisation method.
    for rule in regex_rules():
        result = rule(noun)
        if result:
            return result

def pluralize(noun):
    return plural(noun)

def singularize(word):
    # taken from:http://codelog.blogial.com/2008/07/27/singular-form-of-a-word-in-python/
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
              lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
              lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
              lambda w: w[-2:] == 'es' and w[:-2],
              lambda w: w[-1:] == 's' and w[:-1],
              lambda w: w,
              ]
    word = word.strip()
    singleword = [f(word) for f in sing_rules if f(word) is not False][0]
    return singleword

def check_for_dir( path ):
    ret = False
    #print "check_for_dir(" + os.path.normpath(path) + ")"
    if os.path.isdir( os.path.normpath(path) ):
        ret = True
        #print "is a dir"
    else:
        ret = False
        #print "is NOT a dir"
    return ret


def check_create_dir( path ):
    ret = -1
    #print "checking for " + path +"...\t" ,
    if os.path.isdir( os.path.normpath(path) ):
        print" exists" +"...\t",
        ret = -1
    else:
        os.mkdir( os.path.normpath(path) )
        print " created" +"...\t",
        ret = 1
    print os.path.normpath(path)
    return ret

def check_for_file( path, filename ):
    ret = -1
    if os.path.isfile( os.path.normpath(path + filename) ):
        ret = 1
    else:
        ret = -1
    return ret



def check_create_file( path, filename ):
    ret = -1
    #print "checking for " + os.path.normpath(path + filename) + "...\t" ,
    if os.path.isfile( os.path.normpath(path + filename) ):
        print" exists" +"...\t",
        ret = -1
    else:
        file = open(os.path.normpath(path + filename),"w")
        file.close()
        print " created" +"...\t",
        ret = 1
    print os.path.normpath(path + filename)
    return ret


def check_copy_file( src, dest, force=True, details=False):
    ret = -1
    #print "checking copy of :" + os.path.normpath(src) + "..." ,
    #if os.path.isfile(os.path.normpath(src)):
    #    print "exist\t",
    #else:
    #    print "ERROR: non existent"
    #    sys.exit(-1)
    #print "to " + os.path.normpath(dest)  + "..." ,
    #print "check_copy_file"
    #print src
    #print dest
    if os.path.isfile(os.path.normpath(dest +"/" + src )) and force == False:
        ret = -1
        src_path, src_file = os.path.split(src)
        print " exists ...\t", src_file
        return ret
    else:
        if not check_for_dir(src):
            try:
                shutil.copy(src,dest)
                ret = 1
                print " copied" + "...\t", src
            except IOError, (errno, strerror):
                print " I/O error...(%s): %s. File: %s" % (errno, strerror, src)
                ret = -1
                return ret
        else:
            print " skipped...DIR\t", src

    #print src + " to " + os.path.normpath(dest)
    #src_path, src_file = os.path.split(src)
    #dest_path, dest_file = os.path.split(dest)
    #print src_file
    #print " ---> to ", os.path.join(os.path.relpath(dest_path), dest_file)
    return ret


def create_empty_file( path, filename ):
    file = open(os.path.normpath(path) + filename,"w")
    file.close()


def version_to_string( ver ):
    version = None
    ver = abs(ver)
    if ver < 10:
        version = "0000" + str(ver)
    elif (ver >= 10 and ver < 100):
        version = "000" + str(ver)
    elif (ver >= 100 and ver < 1000):
        version = "00" + str(ver)
    elif (ver >= 1000 and ver < 10000):
        version = "0" + str(ver)
    elif (ver >= 10000 and ver < 100000):
        version = str(ver)
    else:
        version = "99999_max_version_number"
    return version


def readconfig(file, section, option, basepath = None):
    config = ConfigParser.ConfigParser()
    path = ""
    if basepath == None:
        if os.path.exists(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../config/") +  file)):
            path = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../config/") +  file)
        elif os.path.exists(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"./config/") +  file)):
            path = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"./config/") +  file)
        else:
            path = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../config/") +  file)
    else:
        if os.path.exists(os.path.abspath(os.path.join( basepath,"./config/") +  file)):
            path = os.path.abspath(os.path.join( basepath,"./config/") +  file)

    config.read(os.path.normpath( path ))
    option = config.get(section, option)
    return option


def read_db_config( file, env ):
    config = ConfigParser.ConfigParser()
    if os.path.exists(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../config/") +  file)):
        config.read(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../config/") +  file))
    elif os.path.exists(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"./config/") +  file)):
        config.read(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"./config/") +  file))
    else:
        path = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../config/") +  file)
        config.read(os.path.normpath( path ))

    opts = ["dialect", "driver", "database", "host", "port", "parameters", "username", "password"]

    dic = {}
    for val in opts:
        dic[val] = config.get(env, str(val) )
    return dic



def op(filename):
    # a short name for os.path.normpath(filename)
    return os.path.normpath(filename)

def get_app_dir():
    #appdir = readconfig("pow.cfg","global","APP_DIR")
    appdir = os.path.abspath( os.path.dirname( __file__ ) + "/../" )
    #print appdir
    return appdir


def get_app_db_conn_str():
    #appdir = readconfig("pow.cfg","global","APP_DIR")
    appdir = get_app_dir()
    return "sqlite:///" + os.path.abspath(appdir + "/db//app.db" )


def get_db_conn_str():
    #env = readconfig("pow.cfg","global","ENV")
    env = pow.global_conf["ENV"]
    #appdir = readconfig( "pow.cfg","global","APP_DIR")
    appdir = get_app_dir()
    #print "APP_DIR: " + appdir
    #print "reading db_conn_str for environment: " + env

    #dic = read_db_config( "db.cfg", env )
    dic = eval("db."+env)
    # debug printing
    #for key in dic:
    #    print key + " : " + dic[key]
    if dic["dialect"] == "sqlite":
        db_conn_str = "sqlite:///" + op(appdir + "/db//" + dic["database"]  + ".db")

    else:
        #The URL is a string in the form
        #            dialect+driver://user:password@host/dbname[?key=value..],
        #where dialect is a database name such as mysql, oracle, postgresql, etc., and driver the
        #name of a DBAPI, such as psycopg2, pyodbc, cx_oracle, etc. Alternatively, the URL can be an
        # instance of URL.

        # see all ssqlalchemy db options here :
        # http://www.sqlalchemy.org/docs/core/engines.html#database-engine-options
        db_conn_str = dic["dialect"]
        if dic["driver"] != "":
            db_conn_str += "+" + dic["driver"]
        db_conn_str += "://"
        if dic["username"] != "":
            db_conn_str += dic["username"] + ":" + dic["password"]
        if dic["host"] != "":
            db_conn_str += "@" + dic["host"]
        db_conn_str += "/" + dic["database"]
    return db_conn_str


def load_class( module_name, class_name):
    #print "split:" + str(file.split(".")[0])
    aclass = None
    amodule = load_module(module_name)
    if hasattr(amodule, class_name):
        aclass = eval("amodule." + class_name + "()")
    return aclass

def load_module( module_name ):

    amodule = None
    #print "split:" + str(file.split(".")[0])
    amodule = __import__( module_name , globals(), locals(), [], -1)
    return amodule

def load_func( module_name, class_name, func_name ):
    aclass = load_class( module_name, class_name )
    afunc = None
    if hasattr( aclass, func_name ):
        afunc = eval("aclass." + func_name)
    return afunc

def print_object( obj ):
    print obj
    print " object  - callable? "
    print "---------------------------------"
    for attr in dir(obj):
        print attr +" - " + str ( callable(attr) )

def check_iscallable( obj ):
    isok = callable(eval(obj))
    print "is callable <" + str ( obj )+ "> :" + str ( isok )
    return isok

def dh(instr):
    ostr = instr
    ostr = str.replace("<", "|")
    ostr = str.replace(">", "|")
    return ostr

def print_sorted( sequence_type ):
    for elem in sorted(sequence_type):
        print elem
    return

def table_to_model(tablename):
    return str.capitalize(singularize(str.lower(tablename)))

def model_to_table(modelname):
    return pluralize(str.lower(modelname))
