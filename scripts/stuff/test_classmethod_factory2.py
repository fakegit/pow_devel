import validate

class Post(object):
    def __init__(self):
        # This is the "base" constructor.
        pass
    
    @property
    def title(self):
        return self._title
        
    @title.setter
    def title(self, title):
        print "check"
        self._title = title

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


p = Post()
print p
print dir(p)
p.title = "test"
print p.title
p.set_some_val(10)
p.set_int_only(12)