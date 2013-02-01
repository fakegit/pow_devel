import validate
import sys
import pymongo

class BasePost(object):
    def __init__(self):
        # This is the "base" constructor.
        pass
    @classmethod
    def init(klass):
        # This is one special constructor.
        self = klass()
        self.foo = 123
        self.title = ""
        return self

    def find(self):
        return foo
            
    rules = {
        'x': lambda(x): len(x) > 0,
        'y': lambda(y): y is not None,
        'z': lambda(z): z is not None and len(z) > 3,
    }

    @validate.validate_required(rules)
    def set_some_val(self, val):
        print "do something with val"
    
    @validate.validate_is_int()
    def set_int_only(self, val):
        print "do something with integer values"

class Post(BasePost):
    # This does some necessary customizations.
    def my_find(self):
        print "my find"
    
    #@property
    #def title(self):
    #    return self._title
        
    #@title.setter
    #def title(self, title):
    #    print "check"
    #    self._title = title


conn = pymongo.Connection()
db = conn.

p = Post.init()
print p
print dir(p)
p.title = "test"
print "p.title:", p.title
p.set_some_val(10)
p.set_int_only(12)