 #!/usr/bin/env python
"""Generates a sequence of tokens from plaintext"""

#define the Environment class
class Environment:
    def __init__(self, enclosing=None):
        #fetch the Skiylia class so we have access to it's functions
        from PySkiylia import Skiylia
        self.skiylia = Skiylia()
        #create a dictionary to store variables
        self.values = dict()
        #store the encolsing Environment
        self.enclosing = enclosing

    #define a way of assigning a value to a stored datatype
    def assign(self, name, value):
        #if the name is in our dictionary
        if name.lexeme in self.values:
            #overwrite the value
            self.values[name.lexeme] = value
            return
        #if we couldn't assign the variable, and we are not the global scope
        if self.enclosing != None:
            #try to assign to our parent scope
            self.enclosing.assign(name, value)
            return
        #else throw an error
        raise RuntimeError([name, "Undefined variable '"+name.lexeme+"'."])

    #define a way to fetch the value of a variable
    def fetch(self, name):
        #check if the variable has been defined
        if name.lexeme in self.values:
            #return the value
            return self.values[name.lexeme]
        #if we didn't find the variable, and we are not the global scope
        if self.enclosing != None:
            #see if the parent scope can find anything
            return self.enclosing.fetch(name)
        #otherwise throw an error
        raise RuntimeError([name, "Undefined variable '"+name.lexeme+"'."])

    #define a way of defining a variable
    def define(self, name, value):
        #either create or overwrite the dictionary value
        self.values[name] = value
