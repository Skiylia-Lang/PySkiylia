 #!/usr/bin/env python
"""Generates a callable object"""

#define the class
class SkiyliaCallable:
    arity=0
    string=""
    #initialiser
    def __init__(self, callee=""):
        #we're given the callee name
        pass

    def __str__ (self):
        return "<{}>".format(self.string)

    #define the way of calling the function
    def call(self, interpreter, arguments):
        #we're given the interpreter state in case we need it's memory
        pass
