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

    def AssignExpr(self, expr):
        pass

    def BinaryExpr(self, expr):
        pass

    def BlockStmt(self, stmt):
        self.beginScope()
        self.resolve()
        pass

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

    def VarStmt(self, stmt):
        pass

    def WhileStmt(self, stmt):
        pass
