#!python
#
# simple_server is a simple wsgi server for testing purposes only.
# Gives you the opportunity to develop on your local machine 
# without any complex Webserver / module configuration at first.
#
# DO NOT USE THIS for production. !!!!
# 


from wsgiref.simple_server import make_server

import string
import os.path
import sys
import os
import re
from pprint import pformat
from beaker.middleware import SessionMiddleware
#from cgi import parse_qs, escape
import cgi

import traceback, StringIO
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./config" )))
import urllib
import pow
import powlib
import pow_web_lib
from webob import Request, Response

# one of: 
#    NORMAL  = print almost nothing
#    INFO    = more Info printed (But especially NOT the whole WSGI environment)
#    DEBUG   = All Info printed, including WSGI environment. (LONG)
MODE_NORMAL = 1
MODE_INFO = 2
MODE_DEBUG = 3

MODE = MODE_NORMAL

def powapp_simple_server(environ, start_response):
    
    #print show_environ_cli(environ)
    output = []
    powdict =  {}    
    real_action = None
    
    req = Request(environ)
    req.charset = pow.global_conf["DEFAULT_ENCODING"]
    #print "webob: req.params", req.params
    #print "webob: req.body", req.body
    
    
    #print dir(req.params)
    #
    # relevant parameters have to be defined here
    # (Same as for apache the declarations in the httpd.conf file
    #
    # redirect static media from the meta link static to the real source dir
    # advantage is: you can alway refer safely to /static/<something> inside your css o .tmpl
    # files and the real source can be anywhere. sometimes the real static source differs from
    # prod-webserver A to prod-webserver B. with this litte tirck you can leave your links unchanged.
    # for apache the redirection is done in http.conf
    alias_dict ={    
        "/static/css/"             :    "./public/css/",
        "/static/stylesheets/"     :    "./public/css/",
        "/static/scripts/"         :     "./public/js/",
        "/static/js/"               :     "./public/js/",
        "/static/documents/"     :     "./public/doc/",
        "/static/doc/"           :     "./public/doc/",
        "/static/ico/"           :     "./public/ico/",
        "/static/img/"           :     "./public/img/"
        
        }
    environ["SCRIPT_FILENAME"] = __file__
    powdict["POW_APP_NAME"] = "#POWAPPNAME"
    powdict["POW_APP_URL"] = "www.pythononwheels.org"
    powdict["POW_APP_DIR"] = environ.get("pow.wsgi_dir")
    powdict["ERROR_INFO"] = "NONE"
    
    # Get the session object from the environ
    session = environ['beaker.session']
    #TO_DO: set the right status in the end, according to the situatio instead of setting it hard-coded here
    status = '200 OK'
    response_headers = [
        #('Content-type', 'text/html; charset=utf-8')
        ('Content-type', 'text/html')
        ]

    
    if not session.has_key('user.id'):
        session['user.id'] = 0
    
    #session.save()
    
    powdict["SESSION"] = session
    print "-- request info:"
    print "-- webob: req.content_type: ", req.content_type
    print "-- webob: ", req.method
    
    powdict["REQ_CONTENT_TYPE"] = req.content_type
    powdict["REQ_PARAMETERS"] = req.params
    powdict["REQ_BODY"] = req.body
    
    print powdict["REQ_PARAMETERS"]
    
    if MODE > MODE_NORMAL: 
        print plist
        print plist.keys()
    plist = req.params
    
    #if plist.has_key("image"):
    #    print "Image found: ", plist['image'].filename
    #    ofile = file(plist['image'].filename, "wb")
    #    infile = plist['image'].file
    #    ofile.write( infile.read() )
    #   #ofile.write( plist["image"].value )
    #    ofile.close()
    #
    # handling static files
    #
    pinfo = environ.get("PATH_INFO")
    pinfo_before = pinfo
    ostr = ""
    #
    # check for static links and replace them when found.
    #
    found_static = False
    for elem in alias_dict:
        if string.find(pinfo,  elem) != -1:
            found_static = True
            pinfo = string.replace(pinfo,elem, alias_dict[elem])
    
    environ["PATH_INFO"] = pinfo
    
    if found_static == True:
        print "-- Static REQUEST --------------------------------------------------------- "
        non_binary = [".css", ".html",".js",".tmpl"]
        ctype = "UNINITIALIZED"
        ftype = os.path.splitext(pinfo)[1]
        
        if string.lower(ftype) in non_binary:
            infile = open (os.path.normpath(pinfo), "r")
        else:
            infile = open (os.path.normpath(pinfo), "rb")
        ostr = infile.read()
        infile.close()
        #print "file type is: ", ftype, " -> ", ctype
        if string.lower(ftype) == ".gif":
            ctype = "image/gif"
        elif string.lower(ftype) == ".jpg" or string.lower(ftype) ==".jpeg":
            ctype= "image/jpeg"
        elif string.lower(ftype) == ".css":
            ctype = "text/css"
        elif string.lower(ftype) == ".png":
            ctype = "image/png"
        elif string.lower(ftype) ==".js":
            ctype= "application/x-javascript"
        else:
            ctype = "text/html"
        #print "file type is: ", ftype, " responding with type-> ", ctype
        response_headers = [
            ('Content-type', ctype )
        ]
        start_response(status, response_headers)
        return [ostr]
        
    print "-- Dynamic REQUEST --------------------------------------------------------- "
    if MODE > MODE_INFO :
        print "Request: " + environ["REQUEST_METHOD"] + " " + environ["PATH_INFO"] + " " + environ["SERVER_PROTOCOL"] + " " + environ["QUERY_STRING"]    
        print "PATH_INFO before: ", pinfo_before
        print "PATH_INFO after: ", pinfo
        
    if not session.has_key('counter'):
        session['counter'] = 0
    else:
        session['counter'] += 1

    powdict["SCRIPT_FILENAME"] = environ.get("SCRIPT_FILENAME")
    powdict["SCRIPT_DIR"] = os.path.dirname(environ.get("SCRIPT_FILENAME"))
    powdict["SCRIPT_VIEWS_DIR"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/"))
    # PATH_INFO contains the path beginning from the app-root url.     # first part is the controller,      # second part is the action
    powdict["PATH_INFO"] = environ.get("PATH_INFO")
    #print os.path.split(powdict["PATH_INFO"])
    powdict["ENVIRON"] = pow_web_lib.show_environ( environ )
    powdict["DOCUMENT_ROOT"] = environ.get("DOCUMENT_ROOT")
    powdict["FLASHTEXT"] = ""
    powdict["FLASHTYPE"] ="error"
    #output.append( show_environ( output, environ ) )
    
    #
    # get controller and action
    #
    print "environ[\"PATH_INFO\"] = ", environ["PATH_INFO"]
    pathdict = pow_web_lib.get_controller_and_action(environ["PATH_INFO"])
    #(controller,action) = os.path.split(pathinfo)
    print "(controller,action) -> ", pathdict
    controller = powdict["CONTROLLER"] = pathdict["controller"]
    action = powdict["ACTION"] = pathdict["action"]
    powdict["PATHDICT"]=pathdict

    #TO_DO: include the real, mod re based routing instead of seting it hard to user/list here.
    if controller == "":
        defroute = pow.routes["default"]
        #defroute = powlib.readconfig("pow.cfg","routes","default")
        print pow_web_lib.get_controller_and_action(defroute)
        pathdict = pow_web_lib.get_controller_and_action(defroute)
        #(controller,action) = os.path.split(pathinfo)
        print "(controller,action) -> ", pathdict
        controller = powdict["CONTROLLER"] = pathdict["controller"]
        action = powdict["ACTION"] = pathdict["action"]
        powdict["PATHDICT"]=pathdict

        print "Using the DEFAULT_ROUTE: ",
        print "(controller,action) -> ", pathdict
    # get rid of the first / in front of the controller. string[1:] returns the string from char1 to len(string)
    controller = string.capitalize(controller) + "Controller"
    
    #
    # route the request
    #
    #print "Loading Class:", controller
    aclass = powlib.load_class(controller,controller)
    #print "setting Action: ", action
    aclass.setCurrentAction(action)
    #output.append(action + "<br>")
    # checking if action is locked 
    if aclass.is_locked(action):
        # locked, so set the action to the given redirection and execute that instead.
        # TODO: Could be aditionally coupled with a flashtext.
        print "Action: ", action, " locked."
        cont, action = aclass.get_redirection_if_locked(action)
        if  cont != None and cont != "None" and cont != "":
            controller = string.capitalize(cont) + "Controller"
            aclass = powlib.load_class(controller,controller)
        aclass.setCurrentAction(action)
        print " -- Redirecting to: ", action
    #
    # Now really execute the action
    #
    if hasattr( aclass, action ):
        real_action = eval("aclass." + action)  
        output.append(real_action(powdict).encode(pow.global_conf["DEFAULT_ENCODING"]))
    else:
        msg = "ERROR: No such class or action  %s.%s " % (controller, action)  
        output.append(msg)
    #
    # error handling wsgi see: http://www.python.org/dev/peps/pep-0333/#error-handling
    #
    start_response(status, response_headers)
    return output
        
session_opts = {
    'session.type': 'file',
    'session.data_dir': './session_data',
    'session.cookie_expires': True,
    'session.auto': True
}

#application= SessionMiddleware(powapp, key='mysession', secret='randomsecret')
#application = SessionMiddleware(powapp, session_opts)


if __name__ == "__main__":
    application = pow_web_lib.Middleware(SessionMiddleware(powapp_simple_server, session_opts))
    port = pow.global_conf["PORT"]
    httpd = make_server('', int(port), application)
    print "Serving HTTP on port %s..." % (port)

    # Respond to requests until process is killed
    httpd.serve_forever()

    # Alternative: serve one request, then exit
    #httpd.handle_request()
