 #!/usr/bin/env python
"""Define primitive functions here"""

#import python code
import time, math

#import our code
from SkiyliaCallable import SkiyliaCallable
from DataTypes import *

#convert internal representation to user readible code
def stringify(obj):
    print(obj, type(obj), isinstance(obj, SkiyliaInt))
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
    #if the object is an instance, reclaim the class
    if isinstance(obj, SkiyliaInstance):
        obj = obj.thisclass
    #if it's a number
    if isinstance(obj, float) or isinstance(obj, SkiyliaInt):
        #if it's an integer, cast to integer first
        if isinstance(obj, SkiyliaInt):
            return obj.value
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

#typeof
class skiyliatype(SkiyliaCallable):
    string = "primitive"
    arity=1
    callname = "type"
    def call(self, interpreter, arguments, token):
        return type(arguments[0])

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
    arity=1
    callname = "sqrt"
    def call(self, interpreter, arguments, token):
        n = arguments[0]
        try:
            return math.sqrt(n)
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

'''#string conversion
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
        n = arguments[0]
        try:
            return float(int(float(n)))         #skiylia represents all numbers as floats
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

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
        n = arguments[0]
        try:
            return float(n)
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

#boolean conversion
class skiyliabool(SkiyliaCallable):
    string="primitive function"
    arity = 1
    callname = "bool"
    def call(self, interpreter, arguments, token):
        n = arguments[0]
        try:
            return bool(n)
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])'''

#absolute value return
class skiyliaabsolute(SkiyliaCallable):
    string = "primitive function"
    arity = 1
    callname = "abs"
    def call(self, interpreter, arguments, token):
        n = arguments[0]
        try:
            return abs(float(n))
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

#power
class skiyliapow(SkiyliaCallable):
    string = "primitive function"
    arity = 2
    callname = "pow"
    def call(self, interpreter, arguments, token):
        n, m = arguments
        try:
            return float(n) ** float(m)
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

#modulo
class skiyliamod(SkiyliaCallable):
    string = "primitive function"
    arity = 2
    callname = "mod"
    def call(self, interpreter, arguments, token):
        n, m = arguments
        try:
            return float(n) % float(m)
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

#floor
class skiyliafloor(SkiyliaCallable):
    string = "primitive function"
    arity = 1
    callname = "floor"
    def call(self, interpreter, arguments, token):
        n = arguments[0]
        try:
            return float(round(float(n) - .5))
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

#ceil
class skiyliaceil(SkiyliaCallable):
    string = "primitive function"
    arity = 1
    callname = "ceil"
    def call(self, interpreter, arguments, token):
        n = arguments[0]
        try:
            return float(round(float(n) + .5))
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])

#ceil
class skiyliaround(SkiyliaCallable):
    string = "primitive function"
    arity = "1,2"
    callname = "round"
    def call(self, interpreter, arguments, token):
        a, b = (arguments+[0])[:2]
        try:
            return float(round(float(a), int(b)))
        except Exception as e:
            raise RuntimeError([token, str(e), type(e).__name__])
