 #!/usr/bin/env python
"""Resolves code variables before runtime"""

#import python functions
from collections import deque

#import our code
from AbstractSyntax import *
from ASTPrinter import Evaluator

#define the Resolver class
class Resolver(misc, Evaluator):
    ##initialise
    def __init__(self, skiylia, interpreter, arglimit):
        #return a method for accessing the skiylia class
        self.skiylia = skiylia
        #make sure we can access the interpreter
        self.interpreter = interpreter
        #define the maximum number of allowed arguments in a function call
        self.arglimit = arglimit
        #define the scope stack
        self.scopes = deque()

    def AssignExpr(self, expr):
        pass

    def BinaryExpr(self, expr):
        pass

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
        pass

    def ExpressionStmt(self, stmt):
        pass

    def FunctionStmt(self, stmt):
        pass

    def IfStmt(self, stmt):
        pass

    def LiteralExpr(self, expr):
        pass

    def LogicalExpr(self, expr):
        pass

    def GroupingExpr(self, expr):
        pass

    def ReturnStmt(self, stmt):
        pass

    def UnaryExpr(self, expr):
        pass

    def VarExpr(self, expr):
        pass

    #declare variables?
    def VarStmt(self, stmt):
        #declare the variable
        self.declare(stmt.name)
        #if it's not empty
        if stmt.initial != 0.0:
            #resolve it's value
            self.resolve(stmt.initial)
        #define the variable
        self.define(stmt.name)
        return None

    def WhileStmt(self, stmt):
        pass

    #create a local scope
    def beginScope(self):
        #add to the top of the stack
        self.scopes.append(dict())

    #remove a local scope
    def beginScope(self):
        #remove from the top of the stack
        self.scopes.pop()

    #declare names into the scope
    def declare(self, name):
        #if we don't have a stack,
        if self.scopes:
            #return empty
            return
        #otherwise add the name to the stack and declare it unusable (each stack position is on top (last index) and is a dict)
        self.scopes[-1][name.lexeme] = False

    #make sure the variable can be used
    def define(self, name):
        if self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

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
