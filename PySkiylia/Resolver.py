 #!/usr/bin/env python
"""Resolves code variables before runtime"""

#import python functions
from collections import deque

#import our code
from AbstractSyntax import *
from ASTPrinter import Evaluator

#define the Resolver class
class Resolver(Evaluator):
    #hold some thingies my dude
    FunctionType = {"None":0, "Function":1, "Method":2}
    ClassType = {"None":0, "Class":1, "Subclass": 2}
    ##initialise
    def __init__(self, skiylia, interpreter, arglimit):
        #return a method for accessing the skiylia class
        self.skiylia = skiylia
        #make sure we can access the interpreter
        self.interpreter = interpreter
        #define the maximum number of allowed arguments in a function call
        self.arglimit = arglimit
        #define the current function as null
        self.currentFunction = self.FunctionType["None"]
        #define the current class as null
        self.currentClass = self.ClassType["None"]
        #define the scope stack
        self.scopes = deque()

    #run the resolver
    def Resolve(self, stmts):
        #create a 'global' scope
        self.beginScope()
        #resolve all statements
        self.resolve(stmts)
        #remove the 'global' scope
        self.endScope()

    #resolve assignments
    def AssignExpr(self, expr):
        #check if the value contains any variables
        self.resolve(expr.value)
        #and then resolve our name
        self.resolveLocal(expr, expr.name)
        return None

    def BinaryExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    #check through the contents of a block
    def BlockStmt(self, stmt):
        #create a new scope
        self.beginScope()
        #resolve the contents of the block
        self.resolve(stmt.statements)
        #finalise the scope
        self.endScope()
        #return none
        return None

    def CallExpr(self, expr):
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)
        return None

    def ClassStmt(self, stmt):
        #store a reference to the enclosing class
        enclosingClass = self.currentClass
        self.currentClass = self.ClassType["Class"]
        #do the class name definition stuff
        self.declare(stmt.name)
        self.define(stmt.name)
        #check if we have been given a superclass
        if stmt.superclass:
            #set our classtype to subclass
            self.currentClass = self.ClassType["Subclass"]
            if stmt.superclass.name.lexeme == stmt.name.lexeme:
                self.error(stmt.superclass.name, "A class cannot be it's own superclass.")
            #then resolve it
            self.resolve(stmt.superclass)
            #ensure we have a reference to our superclass when calling "super"
            self.beginScope()
            self.scopes[-1]["super"] = True
        #create a scope for the class
        self.beginScope()
        #amd stick "self" into it
        self.scopes[-1]["self"] = True
        #all the class method stuffs
        for method in stmt.methods:
            #set the type to method
            declaration = self.FunctionType["Method"]
            #and resolve it
            self.resolveFunction(method, declaration)
        #end the class scope
        self.endScope()
        #and end the superclass scope if we had one
        if stmt.superclass:
            self.endScope()
        #return the class enclosure to what it was
        self.currentClass = enclosingClass
        return None

    def ExpressionStmt(self, stmt):
        #resolve the expression
        self.resolve(stmt.expression)
        return None

    def FunctionStmt(self, stmt):
        #declare the function name
        self.declare(stmt.name)
        #and define it
        self.define(stmt.name)
        #tell the resolver we are now in a function
        self.currentFunction = self.FunctionType["Function"]
        #and resolve the body of the function
        self.resolveFunction(stmt, self.currentFunction)
        return None

    def GetExpr(self, expr):
        self.resolve(expr.object)
        return None

    def GroupingExpr(self, expr):
        self.resolve(expr.expression)
        return None

    def IfStmt(self, stmt):
        #resolve the condition
        self.resolve(stmt.condition)
        #the then branch
        self.resolve(stmt.thenBranch)
        #and if it has an if
        if stmt.elseBranch:
            self.resolve(stmt.elseBranch)
        return None

    def LiteralExpr(self, expr):
        return None

    def LogicalExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def ReturnStmt(self, stmt):
        #if we aren't in a function
        if self.currentFunction == self.FunctionType["None"]:
            #throw an error
            self.error(stmt.keyword, "Can't return from top-level code")
        #if the return statement has a value
        if stmt.value:
            #return that
            self.resolve(stmt.value)
        return None

    def SelfExpr(self, expr):
        #ensure we are in a class first
        if self.currentClass == self.ClassType["None"]:
            self.error(expr.keyword, "Can't use 'self' outside of a class")
        #return the value
        self.resolveLocal(expr, expr.keyword)
        return None

    def SetExpr(self, expr):
        #resolve the value for the set
        self.resolve(expr.value)
        #and resolve the property it is refering to
        self.resolve(expr.object)
        return None

    def SuperExpr(self, expr):
        if self.currentClass == self.ClassType["None"]:
            self.error(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.currentClass == self.ClassType["Class"]:
            self.error(expr.keyword, "Can't use 'super' within a class with no superclass.")
        self.resolveLocal(expr, expr.keyword)
        return None

    def UnaryExpr(self, expr):
        self.resolve(expr.right)
        return None

    #calling variables
    def VarExpr(self, expr):
        #check that the scope exists, and that the variable has been initialised
        if bool(self.scopes) and (expr.name.lexeme in self.scopes[-1]) and (self.scopes[-1][expr.name.lexeme]==False):
            #if it hasn't, and the scope exists, throw an error
            self.error(expr.name, "Can't read local variable in its own initialiser")
        #otherwise resolve the local variables
        self.resolveLocal(expr, expr.name)
        return None

    #declare variables?
    def VarStmt(self, stmt):
        #declare the variable
        self.declare(stmt.name)
        #if it's not empty
        if stmt.initial:
            #resolve it's value
            self.resolve(stmt.initial)
        #define the variable
        self.define(stmt.name)
        return None

    def WhileStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    #create a local scope
    def beginScope(self):
        #add to the top of the stack
        self.scopes.append(dict())

    #remove a local scope
    def endScope(self):
        #remove from the top of the stack
        self.scopes.pop()

    #declare names into the scope
    def declare(self, name):
        #if we don't have a stack,
        if not bool(self.scopes):
            #return empty
            return
        #if the variable has already been declared
        if name.lexeme in self.scopes[-1]:
            #chuck an error
            self.error(name, "Variable with this name already in scope.")
        #otherwise add the name to the stack and declare it unusable (each stack position is on top (last index) and is a dict)
        self.scopes[-1][name.lexeme] = False

    #make sure the variable can be used
    def define(self, name):
        #if the scope exists, we can continue
        if not bool(self.scopes):
            return
        #mark the variable as initialised
        self.scopes[-1][name.lexeme] = True

    #resolve the body of a function
    def resolveFunction(self, function, funcType):
        #get the function type of the parent
        enclosingFunction = self.currentFunction
        #and set the internal representation to our function type
        self.currentFunction = funcType
        #create a scope for the function
        self.beginScope()
        #loop through the parameters
        for param in function.params:
            #declare and define
            self.declare(param)
            self.define(param)
        #and then resolve the body
        self.resolve(function.body)
        #finally end the local scope
        self.endScope()
        #and reset the function type of the parent to current
        self.currentFunction = enclosingFunction

    #resolve is something is local, or furthe rup the scope
    def resolveLocal(self, expr, name,):
        #itterate through the scopes, starting from the top of the stack (the final index)
        for x in range(len(self.scopes))[::-1]:
            #if the local is found here
            if name.lexeme in self.scopes[x]:
                #return None in the distance from the current scope to the one where the variable was found
                self.interpreter.resolve(expr, len(self.scopes) - x - 1)# - (self.currentFunction==1)) # <-piece of hacky code that worked on a single occasion
                return

    #loop through provided statements
    def resolve(self, stmts):
        #if we have an itterable
        if isinstance(stmts, list):
            #loop through all given
            for stmt in stmts:
                #and call the evaluation
                self.evaluate(stmt)
        else:
            #otherwise use the singular
            self.evaluate(stmts)

    #define a way of showing errors to the user
    def error(self, token, message):
        #if we reached the end of the file, show an EOF error
        if token.type == "EOF":
            self.skiylia.error(token.line, token.char, message, "at end of file, Syntax")
        #otherwise show the user what the exact location and token was
        else:
            self.skiylia.error(token.line, token.char, message, "at '"+token.lexeme+"', Syntax")
        #and return our base resolver error
        return [token, message, "Resolve"]
