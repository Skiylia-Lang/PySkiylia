 #!/usr/bin/env python
"""Generates callable objects"""
from Environment import Environment

#the return exception class for
class Return(Exception):
    def __init__(self, value):
        self.message = value

#define the callable class
class SkiyliaCallable:
    arity=0
    string=""
    callname = ""
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

#internal handling of functions
class SkiyliaFunction(SkiyliaCallable):
    string = "Skiylia function"
    def __init__(self, declaration):
        #define the internals at initialisation
        self.callname = declaration.name.lexeme
        self.declaration = declaration
        self.arity = len(self.declaration.params)

    def call(self, interpreter, arguments):
        #create a new local scope based on the global one
        self.environment = Environment(interpreter.globals)
        #loop through all of our defined parameters
        for x in range(len(self.declaration.params)):
            #add them to our local environment
            self.environment.define(self.declaration.params[x].lexeme, arguments[x])
        #as we're handling returns using exceptions, we need a try
        try:
            #ask the interpreter to execute the block
            interpreter.executeBlock(self.declaration.body.statements, self.environment)
        except Return as ret:
            #if we had a return, return the contents
            return ret.message
        #return None by default
        return None
