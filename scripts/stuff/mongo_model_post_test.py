#
#
# Modelclass for PoW on MongoDB
#
#
import sys
import os
import os.path


sys.path.append(os.path.normpath(os.path.join(__file__, "../models" )) )
sys.path.append(os.path.normpath(os.path.join(__file__, "../lib" )) )
sys.path.append(os.path.normpath(os.path.join(__file__, "../config" )) )
#import pow
#import powlib
import mongo_basemodel
from pow_base_object import PowBaseObject


class Post(mongo_basemodel.BaseModel):

    """
        Default Model class for PythonOnWheels on MongoDB
    """

    def __init__(self):
        pass

    # @property
    # def title(self):
    #     return self._title

    # @title.setter
    # def title(self, val):
    #     print "in property setter"
    #     self._title = val