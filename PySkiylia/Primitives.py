 #!/usr/bin/env python
"""Define primitive functions here"""

#import python code
import time

#import our code
from SkiyliaCallable import SkiyliaCallable

#clock
class clock(SkiyliaCallable):
    #define the function stuff
    arity=0
    string="primitive function"
    #and overwite the call
    def call(self, interpreter, arguments):
        return time.time()
