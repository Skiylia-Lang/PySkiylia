 #!/usr/bin/env python
"""Generates callable objects"""
from Environment import Environment

#the return exception class for
class Return(Exception):
    def __init__(self, value):
        self.message = value

#the interupt exception class
class Interupt(Exception):
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
    def call(self, interpreter, arguments, token=""):
        #we're given the interpreter state in case we need it's memory
        pass

class SkiyliaArray(SkiyliaCallable):
    arity = "0,*"
    string = "Skiylia array"
    callname = "Array"
    def __init__(self, *elements):
        self.name = "array"
        self.list = list(elements)
        self.instance = SkiyliaInstance(self)
        self.instance.get = self.get

    def get(self, name):
        #construct a new callable
        a = SkiyliaCallable()
        #setup the base parameters
        a.arity = 0
        a.string = "Skiylia array function"
        a.callname = name.lexeme
        #if the user wants to get from a function
        if name.lexeme == "get":
            #setup the base parameters
            a.arity = 1
            #create it's call function
            def newcall(interpreter, arguments, token=""):
                try:
                    #return the list index they asked for
                    return self.list[int(arguments[0])]
                except:
                    #or show them an error if it wasn't valid
                    raise SyntaxError([token, "Invalid index '{}' for array.".format(arguments[0])])
        #if the user wants to pop from a function
        elif name.lexeme == "pop":
            #create it's call function
            def newcall(interpreter, arguments, token=""):
                #remove the last index and return it
                return self.list.pop()
        #if the user wants to remove from a function
        elif name.lexeme == "remove":
            #setup the base parameters
            a.arity = 1
            #create it's call function
            def newcall(interpreter, arguments, token=""):
                try:
                    #fetch the index
                    idx = int(arguments[0])
                    #if its within the array, then overwrite
                    return self.list.pop(idx)
                except:
                    #or show them an error if it wasn't valid
                    raise SyntaxError([name, "Invalid index '{}' for array.".format(arguments[0])])
        elif name.lexeme == "add":
            #setup the base parameters
            a.arity = 1
            #create it's call function
            def newcall(interpreter, arguments, token=""):
                ##append their value to the list
                self.list.append(arguments[0])
                #and return the list
                return self.list
        #elseif the user wants to set at an index
        elif name.lexeme == "set":
            #setup the base parameters
            a.arity = 2
            #create it's call function
            def newcall(interpreter, arguments, token=""):
                try:
                    #fetch the index
                    idx = int(arguments[0])
                    #if its within the array, then overwrite
                    if idx < len(self.list):
                        self.list[idx] = arguments[1]
                    #if it's the length of the array, append
                    elif idx == len(self.list):
                        self.list.append(arguments[1])
                    #if not, then throw an error
                    else:
                        raise SyntaxError([name, "Index '{}' outside of array.".format(arguments[0])])
                    #return the list if no error was raised
                    return self.list
                except:
                    #or show them an error if it wasn't valid
                    raise SyntaxError([name, "Invalid index '{}' for array.".format(arguments[0])])
        #elseif the user wants to insert at an index
        elif name.lexeme == "insert":
            #setup the base parameters
            a.arity = 2
            #create it's call function
            def newcall(interpreter, arguments, token=""):
                try:
                    #fetch the index
                    idx = int(arguments[0])
                    #if its within the array, then overwrite
                    self.list.insert(idx, arguments[1])
                except:
                    #or show them an error if it wasn't valid
                    raise SyntaxError([name, "Invalid index '{}' for array.".format(arguments[0])])
                #return the list if no error was raised
                return self.list
        elif name.lexeme == "len":
            #create it's call function
            def newcall(interpreter, arguments, token=""):
                return len(self.list)
        elif name.lexeme == "join":
            a.arity = "1,*"
            def newcall(interpreter, arguments, token=""):
                for x in arguments:
                    #check if we are joining an array
                    if isinstance(x, SkiyliaCallable) and ("Skiylia array" in x.string):
                        for y in x.thisclass.list:
                            self.list.append(y)
                        continue
                    #else default to array.add()
                    self.list.append(x)
                #return the list
                return self.list
        #overwrite the call function with our new array one
        a.call = newcall
        #and return the callable
        return a

#array shorthand
class SkiyliaArr(SkiyliaArray):
    callname = "Arr"

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
            if self.isinit and (ret.message is None):
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
        environment.define("self", instance)
        #and return the new function with that environment
        return SkiyliaFunction(self.declaration, environment, self.isinit)

#internal handling of classes
class SkiyliaClass(SkiyliaCallable):
    #what to print
    string = "skiylia class"
    #initialiser
    def __init__(self, name=None, superclass=None, methods=[]):
        #assign our name
        self.name = name
        self.superclass = superclass
        self.methods = methods
        self.string = "_skiyliaClass.{}".format(name)
        #check for an init method to determine arity
        self.initialiser = self.findMethod("init")
        #if we have one
        if self.initialiser:
            #define our arity
            self.arity = self.initialiser.arity
    #what to do when we call the class
    def call(self, interpreter, arguments, token=""):
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
        #otherwise check in our superclass if we have one
        elif self.superclass:
            return self.superclass.findMethod(name)
        #otherwise return none
        return None

    def bind(self, instance):
        #return a class reference
        return SkiyliaClass(self.name, None, self.methods)

#internal handling of modules
class SkiyliaModule(SkiyliaCallable):
    #what to print
    string = "skiylia module"
    #initialiser
    def __init__(self, name=None, methods=[]):
        #assign our name, methods, and string
        self.name = name
        self.methods = methods
        self.string = "_skiyliaModule.{}".format(name)
        #create an instance, so we can call funtions
        self.instance = SkiyliaInstance(self)

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
        self.classtype = type(thisclass)
        #the string that will be printed
        self.string = "{}.{}_instance".format(thisclass.string.split(".")[0], thisclass.name)
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
        #if it is a method instead
        if method:
            #return that
            return method.bind(self)
        #else throw an error
        raise RuntimeError([name, "Undefined property '{}'.".format(name.lexeme)])

    #set the value of a property with a given name
    def set(self, name, value):
        #set the internal field to the correct value for the property name
        self.fields[name.lexeme] = value
