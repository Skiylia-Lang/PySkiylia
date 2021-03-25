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
    def __init__(self, declaration, closure):
        #define the internals at initialisation
        self.closure = closure
        self.declaration = declaration
        self.arity = len(self.declaration.params)

    def call(self, interpreter, arguments):
        #create a new local scope based on the enclosing one
        self.environment = Environment(self.closure)
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

#internal handling of classes
def SkiyliaClass(SkiyliaCallable):
    #what to print
    string = "skiylia class"
    #initialiser
    def __init__(self, name):
        #assign our name
        self.name = name
        self.string = "_skiyliaClass.{}".format(name)
    #what to do when we call the class
    def call(self, interpreter, arguments):
        #create a new instance of the class
        instance = SkiyliaInstance(self)
        #and return it
        return instance

#internal instance handling
def SkiyliaInstance(SkiyliaCallable):
    def __init__(self, thisclass):
        #store the class that this instance is attatched to
        self.thisclass = thisclass
        self.string = "_skiyliaClass.{}_instance".format(thisclass.name)
