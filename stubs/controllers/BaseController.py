#
#
# DO NOT EDIT THIS FILE.
# This file was autogenerated by python_on_wheels.
# Any manual edits may be overwritten without notification.
#
# 

# date created:     2011-04-27


import sys
import os
from mako.template import Template
from mako.lookup import TemplateLookup


sys.path.append(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../models" )) )
sys.path.append(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )) )
sys.path.append(os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../config" )) )
import pow
import powlib
import PowObject

class BaseController(object):
    #model = None
    #session = None
    #modelname = "None"
    #current_action = "list"
    moddir="/../views/mako_modules"
    #mylookup = None
    
    
    def __init__(self):
        # put the actions that require a login into login_required list.
        self.login_required = []
        # put the actions you implemented but do not want to be callable via web request 
        # into the locked_actions dictionary. Format: "actionname" : "redirect_to" }
        # simple_server and pow_router will not call locked actions but redirect to the given value, instead
        self.locked_actions = {}
        self.current_action = "NOT_DEFINED"
        # Format: { filter: ( selector, [list of actions] ) } 
        self.pre_filter_dict = {}
        
        self.mylookup = TemplateLookup(directories=[os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/")),
                    os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/layouts/")),
                    os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/stylesheets/"))
                    ] )
        # example how to instanciate the model:
        if self.modelname == None or self.modelname == "None":
            self.model = None
            self.session = None
        else:
            self.model = powlib.load_class(self.modelname, self.modelname)
            self.session = self.model.pbo.getSession()
       
        
    
    #def __getattribute__(self, key):
    #   return super(BaseController, self).__getattribute__(key)
    #def __getattribute__(self,name):
    #    # check if pre_filter needs to be applied
    #    if name != '__dict__':
    #        #print '__getattribute__', name
    #        if name in self.__dict__["pre_filter_dict"].keys():
    #            print "filter found"
    #        else:
    #            print "no filter found",  self.__dict__["pre_filter_dict"].keys()
    #            
    #    ret = BaseController.__getattribute__(self,name)
    #    
    #    return ret
    def pre_filter(self, filter, selector ,action_list = []):
        
        """
        set a pre_filter operation for controller actions.
        @param filter:             Name of the filter to be executed before the action (Module.Class.Method) 
                                  if there are no dots self.filter is assumed
        @param selector:           One of: any, except,only
        @param action_list:        If selector is except OR only, this defines the actions in scope.
        """
        # check if filter already set.
        if not self.pre_filter_dict.has_key(filter):
            # check if selector correct
            if selector in ["any", "except", "only"]:
                # set the filter
                if selector == "any":
                    import inspect
                    alist =  inspect.getmembers(self, predicate=inspect.ismethod)
                    for elem in alist:
                        print elem[0]
                elif selector == "only":
                    for func in action_list:
                        if self.pre_filter_dict.has_key(func):
                            self.pre_filter_dict[func].append(filter)
                        else:
                            self.pre_filter_dict[func] = [filter]
                elif selector == "except":
                    pass
                print "Added pre_filter: ", self.pre_filter_dict
                return True
            else:
                raise NameError("selector must be one of: only, except or any. You gave %s" % (str(selector)))
                return False
        return False 
       
    def get_locked_actions(self):
        """ returns the dictionary of locked actions. 
        Locked actions will not be executed by simple_server nor pow_router"""
        return self.locked_actions
    
    def is_locked(self, action):
        """ returns the the True, if the given action is locked. 
        Locked actions will not be executed by simple_server nor pow_router"""
        if self.locked_actions.has_key(action):
            return self.locked_actions[action]
        else:
            return False
        # should never be reached
        return False

    def get_redirection_if_locked(self, action): 
        """returns the redirection, if the given action is locked. None otherwise. 
        Locked actions will not be executed by simple_server nor pow_router"""
        if self.is_locked(action):
            return self.locked_actions[action]
        else:
            return "None"
        # should never be reached
        return "None"
            
    def render(self, **kwargs):
        """
            Renders a template:
            
            Mandatory Parameters:
            powdict    =    The powdict containing all the HTTP:Request Parameters, Body etc.
            
            Optional Parameters:
            special_tmpl     =     a speciaol template to use. By default Controller_current_action.tmpl is chosen 
        """
        powdict = kwargs["powdict"]
        kwargs["powdict"] = powdict
        kwargs["template"] = pow.global_conf["DEFAULT_TEMPLATE"] 

        special_tmpl = None
        if kwargs.has_key("special_tmpl"):
            special_tmpl = kwargs["special_tmpl"]
            del kwargs["special_tmpl"]

        if self.current_action not in self.locked_actions:
            if self.access_granted(**kwargs) == True:
                first_part = os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/")
                if special_tmpl == None:
                    fname =  self.modelname + "_" + self.current_action +".tmpl"
                else:
                    fname =  special_tmpl
                mytemplate = self.mylookup.get_template(fname)
                #mytemplate = Template(filename=fname, lookup=self.mylookup)
                return mytemplate.render(**kwargs)
            else:
                #self.setCurrentAction("login")
                kwargs["powdict"]["FLASHTEXT"] = "You need to be logged in to access method: %s" % (str(self.current_action))
                kwargs["powdict"]["FLASHTYPE"] = "error"
                #fname = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/App_login.tmpl"))
                fname = "App_login.tmpl"
                #mytemplate = Template(filename=fname, lookup=self.mylookup)
                mytemplate = self.mylookup.get_template(fname)
                return mytemplate.render(**kwargs)
        else:
            kwargs["ERROR_INFO"] = "The action you have called (", self.current_action, "is locked from outside access."
            return self.error(**kwargs)
            
    
    def redirect(self, action, **kwargs):
        """ sets the given action and executes it so that all prerequisites are correct """
        self.setCurrentAction(action)
        return eval("self." + action + "(**kwargs)")
    
    def re_route(self, controller, action,**kwargs):
        """ Loads another Controller and calls the given action"""
        kwargs["template"] = pow.global_conf["DEFAULT_TEMPLATE"] 
        controller = None
        controller = powlib.load_class( string.capitalize(controller),string.capitalize(controller))
        if controller != None:
            if hasattr( aclass, action ):
                controller.setCurrentAction(action)
                real_action = eval("controller." + action)
                return real_action(kwargs["powdict"])
            else:
                return render_message("Error, no such action: %s, for controller: %s" % (action, controller), "error", **kwargs)
        else:
            return render_message("Error, no such controller: %s" % (controller), "error", **kwargs)
        return render_message("Error, this should never be reached" % (controller), "error", **kwargs)
    
    def render_message(self, message, type, **kwargs ):
        """Renders the given message using the given type (one of error || success || info || warning)
            as flashmessage, using the error.tmpl. This special tmpl displays the given message alone, embedded
            in the default context.template
            
            Mandatory Parameters:
            message = the flashmessagr
            type    = the type of the message (different css styles)
            powdict = powdict
            Optional:
            tmpl    = a special .tmpl file to use. 
            """
        
        # set the context template.        
        kwargs["template"] = pow.global_conf["DEFAULT_TEMPLATE"] 
        # by default call the error.tmpl. You can give another template using tmpl="template_name.tmpl".

        if kwargs.has_key("tmpl"):
            tmpl = kwargs["tmpl"]
        else:
            tmpl = "error.tmpl"
        # ste the flash messages 
        kwargs["powdict"]["FLASHTEXT"] = message
        kwargs["powdict"]["FLASHTYPE"] = type
        
        mytemplate = self.mylookup.get_template(tmpl)
        return mytemplate.render(**kwargs)
    
    
    def access_granted(self,**kwargs):
        """ 
            returns true if access is ok, meaning that:
            no login required or login required AND user already lgged in.
        """
        powdict = kwargs.get("powdict",None)
        session = powdict["SESSION"]
        is_logged_in = False
        if self.current_action in self.login_required:
            # login required, so check if user is logged in. 
            try:
                if session["user.id"] != 0:
                    return True
            except KeyError:
                    return False
       
        else:
            # no login required
            return True
        # by default return False
        return False
    
        
    def setCurrentAction(self, action ):
        """ sets the cuurent action of this controller to action"""
        self.current_action = action
        