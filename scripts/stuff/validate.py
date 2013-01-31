#
# example decaorator validator for PoW
#


def getInput():
    ''' simulate web.input() for web.py framework '''
    return {
        'x': 'banananaa',
        'y': None,
        'z': 'zz',
    }
    
def validate_required(rules):
    ''' validation decorator '''
    def wrapper(method):
        ''' wrapping the actual method/function '''
        def validate(*args, **kwargs):
            ''' validation take places according to rules '''
            inputs = getInput()
            for k in inputs.keys():
                if k in rules: f = rules[k]
                else: continue
                input = inputs[k]
                if not f(input):
                    out = 'Invalid input %s - %s' % (k, input)
                    print out # or raise Exception here to stop execution
            return method(*args, **kwargs)
        return validate
    return wrapper
    
    
    
def validate_is_int():
    ''' validation decorator '''
    def wrapper(method):
        ''' wrapping the actual method/function '''
        def validate(*args, **kwargs):
            ''' validation take places according to rules '''
            print args
            print kwargs
            if isinstance(args[1], int):
                return method(*args, **kwargs)
            else:
                raise Exception("not an Integer")
        return validate
    return wrapper