#
# generate model
#

import argparse
import tornado.template as template
import os.path
import timeit
import {{appname}}.powlib as lib
import {{appname}}.config as cfg


def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_handler(handler_name, model_type, appname=None):
    """ 
        generates a small handler
    """
    
    #
    # set some attributes
    #
    loader = template.Loader(cfg.templates["stubs_path"])
    handler_class_name = camel_case(handler_name)

    print(40*"-")
    print(" generating handler: " + handler_class_name)
    print(40*"-")
    #
    # create the handler
    #
    if model_type.lower() == "none":
        template_file =  "rest_handler_nodb_template.py"
    else:
        template_file = "rest_handler_template.py"
    ofile_name = os.path.join(cfg.templates["handler_path"], handler_name+".py")
    ofile = open(ofile_name, "wb")
    res = loader.load(template_file).generate( 
        handler_name=handler_name, 
        handler_class_name=handler_class_name,
        handler_model_class_name=handler_class_name,
        model_type = model_type,
        appname=appname,
        )
    ofile.write(res)
    ofile.close()
    print("... created: " + ofile_name)
    print(40*"-")
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="name", help='-n handler name',
                        required=True)
    #
    # db type
    # 
    parser.add_argument('-d', "--db", action="store", 
                        dest="db", help="-d which_db (" + "|| ".join(cfg.database.keys()) + " || none) default=none",
                        default="none", required=False)
    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)
    #print(dir(args))
    print("CamelCased handler name: ", camel_case(args.name))
    generate_handler(args.name, args.db, appname="{{appname}}")

if __name__ == "__main__":
    main()