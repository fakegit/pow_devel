#
#
# Modelclass for PoW on MongoDB
#
#

sys.path.append(os.path.abspath(__file__, "../models" )) 
sys.path.append(os.path.abspath(__file__, "../lib" )) 
sys.path.append(os.path.abspath(__file__, "../config" )) 
import pow
import powlib
from PowBaseObject import PowBaseObject


class #MODELNAME(#BASEMODEL.#BASEMODEL):

    """
        Default Model class for PythonOnWheels on MongoDB
    """

    def __init__(self):
        pass

    #@classmethod
    #def find_by_id(cls, id):
    #    p = cls()
    #    p.pbo = PowBaseObject()
    #    p.db = pbo.get_db()
    #    p.collection = p.db["#DBNAME"] % powlib.pluralize(#MODELNAME)
    #    p.__dict__ = p.collection.find_one({"_id" : id})
    #    return p
    
    #def save(self):
    #    self.collection.save(self.__dict__)