 #!/usr/bin/env python
"""Define primitive functions here"""

#import python code
import time

#import our code
from SkiyliaCallable import SkiyliaCallable

#print function
class skiyliaprint(SkiyliaCallable):
    #define the functional input
    #print can take any number of arguments, but needs at least zero
    arity="0,*"
    string = "primitive function"
    callname = "print"
    #overwrite the call
    def call(self, interpreter, arguments):
        print(*arguments)
        return None

#clock
class clock(SkiyliaCallable):
    #define the function stuff
    arity=0
    string="primitive function"
    #and overwite the call
    def call(self, interpreter, arguments):
        return time.time()
