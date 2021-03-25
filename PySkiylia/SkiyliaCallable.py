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
    def __init__(self, declaration, closure, isinit=False):
        #define the internals at initialisation
        self.closure = closure
        self.declaration = declaration
        self.isinit = isinit
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
            #check if we are an init function, with a blank return
            if self.isinit and (ret.message == None):
                #return a reference to the class
                return self.closure.getAt(0, "self")
            #if we had a return, return the contents
            return ret.message
        #return None by default
        return None

    def bind(self, instance):
        #create a new environment for the method
        environment = Environment(self.closure)
        #add a reference to "self" inside it
        environment.define("self", instance, self.isinit)
        #and return the new function with that environment
        return SkiyliaFunction(self.declaration, environment)

#internal handling of classes
class SkiyliaClass(SkiyliaCallable):
    #what to print
    string = "skiylia class"
    #initialiser
    def __init__(self, name, methods):
        #assign our name
        self.name = name
        self.methods = methods
        self.string = "_skiyliaClass.{}".format(name)
        #check for an init method to determine arity
        self.initialiser = self.findMethod("init")
        #if we have one
        if self.initialiser:
            #define our arity
            self.arity = self.initialiser.arity
    #what to do when we call the class
    def call(self, interpreter, arguments):
        #create a new instance of the class
        instance = SkiyliaInstance(self)
        #if we have an initialiser
        if self.initialiser:
            #then bind it to the class, and call it immediately
            self.initialiser.bind(instance).call(interpreter, arguments)
        #and return it
        return instance
    #lookig for internal methods yo
    def findMethod(self, name):
        #check if the name is one of our methods
        if name in self.methods:
            #if it is, return that
            return self.methods[name]
        #otherwise return none
        return None

#internal instance handling
class SkiyliaInstance(SkiyliaCallable):
    def __init__(self, thisclass):
        #store the class that this instance is attatched to
        self.thisclass = thisclass
        #the string that will be printed
        self.string = "_skiyliaClass.{}_instance".format(thisclass.name)
        #and the internal fields dictionary
        self.fields = dict()

    #fetch properties given name
    def get(self, name):
        #if the name is in our fields
        if name.lexeme in self.fields:
            #return it
            return self.fields[name.lexeme]
        #if the name is not, it may be a class method
        method = self.thisclass.findMethod(name.lexeme)
        #if it is
        if method:
            #return that
            return method.bind(self)
        #else throw an error
        raise RuntimeError([name, "Undefined property '{}'.".format(name.lexeme)])

    #set the value of a property with a given name
    def set(self, name, value):
        #set the internal field to the correct value for the property name
        self.fields[name.lexeme] = value
