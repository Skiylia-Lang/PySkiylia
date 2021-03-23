 #!/usr/bin/env python
"""Define primitive functions here"""

#import python code
import time, math

#import our code
from SkiyliaCallable import SkiyliaCallable

#convert internal representation to user readible code
def stringify(obj):
    #if none, show null
    if obj==None:
        return "null"
    #if the object is boolean
    elif isinstance(obj, bool):
        #if the object is true
        if obj==True:
            return "true"
        #else the object is false
        elif obj==False:
            return "false"
    #if it's a number
    if isinstance(obj, float) or isinstance(obj, int):
        #if it's an integer, cast to integer first
        if obj.is_integer():
            return str(int(obj))
        #else just return it
        return str(obj)
    #return the string of the object
    return str(obj)

#print function
class skiyliaprint(SkiyliaCallable):
    #define the functional input
    #print can take any number of arguments, but needs at least zero
    arity = "0,*"
    string = "primitive function"
    callname = "print"
    #overwrite the call
    def call(self, interpreter, arguments):
        print(*map(stringify, arguments))
        return None

#clock
class skiyliaclock(SkiyliaCallable):
    #define the function stuff
    arity = 0
    string = "primitive function"
    callname = "clock"
    #and overwite the call
    def call(self, interpreter, arguments):
        return time.time()

#sqrt
class skiyliasqrt(SkiyliaCallable):
    arity = 1
    string = "primitive function"
    callname = "sqrt"
    def call(self, interpreter, arguments):
        return math.sqrt(arguments[0])
