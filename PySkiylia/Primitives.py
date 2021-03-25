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

class primitivefunc(SkiyliaCallable):
    string = "primitive function"

#print function
class skiyliaprint(primitivefunc):
    #define the functional input
    #print can take any number of arguments, but needs at least zero
    arity = "0,*"
    callname = "print"
    #overwrite the call
    def call(self, interpreter, arguments):
        print(*map(stringify, arguments))
        return None

#clock
class skiyliaclock(primitivefunc):
    #define the function stuff
    callname = "clock"
    #and overwite the call
    def call(self, interpreter, arguments):
        return time.time()

#sqrt
class skiyliasqrt(primitivefunc):
    callname = "sqrt"
    def call(self, interpreter, arguments):
        return math.sqrt(arguments[0])

#string conversion
class skiyliastring(primitivefunc):
    arity = "0,*"
    callname = "string"
    def call(self, interpreter, arguments):
        return " ".join(str(x) for x in a)

#string shorthand
class skiyliastr(skiyliastring):
    callname = "str"

#integer conversion
class skiyliainteger(primitivefunc):
    arity = 1
    callname = "integer"
    def call(self, interpreter, arguments):
        num = arguments[0]
        try:
            return float(int(float(num)))         #skiylia represents all numbers as floats
        except:
            raise RuntimeError("Cannot convert '{}' to integer.".format(num))

#shorthand for integer
class skiyliaint(skiyliainteger):
    callname = "int"

#float conversion
class skiyliafloat(primitivefunc):
    arity = 1
    callname = "float"
    def call(self, interpreter, arguments):
        num = arguments[0]
        try:
            return float(num)
        except:
            raise RuntimeError("Cannot convert '{}' to integer.".format(num))
