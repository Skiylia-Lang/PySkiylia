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
    string = "primitive function"
    #define the functional input
    #print can take any number of arguments, but needs at least zero
    arity = "0,*"
    callname = "print"
    #overwrite the call
    def call(self, interpreter, arguments, token):
        print(*map(stringify, arguments))
        return None

#clock
class skiyliaclock(SkiyliaCallable):
    string = "primitive function"
    #define the function stuff
    callname = "clock"
    #and overwite the call
    def call(self, interpreter, arguments, token):
        return time.time()

#sqrt
class skiyliasqrt(SkiyliaCallable):
    string = "primitive function"
    callname = "sqrt"
    def call(self, interpreter, arguments, token):
        return math.sqrt(arguments[0])

#string conversion
class skiyliastring(SkiyliaCallable):
    string = "primitive function"
    arity = "0,*"
    callname = "string"
    def call(self, interpreter, arguments, token):
        return " ".join([stringify(x) for x in arguments])

#string shorthand
class skiyliastr(skiyliastring, SkiyliaCallable):
    string = "primitive function"
    callname = "str"

#integer conversion
class skiyliainteger(SkiyliaCallable):
    string = "primitive function"
    arity = 1
    callname = "integer"
    def call(self, interpreter, arguments, token):
        num = arguments[0]
        try:
            return float(int(float(num)))         #skiylia represents all numbers as floats
        except Exception as e:
            raise RuntimeError([token, "Cannot convert '{}' to integer.".format(num)])

#shorthand for integer
class skiyliaint(skiyliainteger, SkiyliaCallable):
    string = "primitive function"
    callname = "int"

#float conversion
class skiyliafloat(SkiyliaCallable):
    string = "primitive function"
    arity = 1
    callname = "float"
    def call(self, interpreter, arguments, token):
        num = arguments[0]
        try:
            return float(num)
        except Exception as e:
            raise RuntimeError([token, "Cannot convert '{}' to float.".format(num)])
