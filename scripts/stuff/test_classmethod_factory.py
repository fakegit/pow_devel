class BasePost(object):
    def __init__(self):
        # This is the "base" constructor.
        pass

    @classmethod
    def init(klass):
        # This is one special constructor.
        self = klass()
        self.foo = 123
        return self


    @classmethod
    def another_constructor(klass, bar):
        # This is another special constructor.
        # ...
        pass
    
    def find(self):
        return foo

class Post(BasePost):
    # This does some necessary customizations.
    def my_find(self):
        print "my find"


p = Post.init()
print p
print dir(p)
print p.foo
print p.my_find()