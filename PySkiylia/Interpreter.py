 #!/usr/bin/env python
"""Generates a sequence of tokens from plaintext"""

#import our code
from Expr import *

#define the Interpreter class
class Interpreter:
    ##initialise
    def __init__(self):
        #fetch the Skiylia class so we have access to it's functions
        from PySkiylia import Skiylia
        self.skiylia = Skiylia()

    #define a way of converting from the literal AST to a runtime value
    def LiteralExpr(self, expr):
        return expr.value

    #define a way of unpacking a grouped expression at runtime
    def GroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    #define a way of unpacking a Unary
    def UnaryExpr(self, expr):
        #fetch the right
        right = self.evaluate(expr.right)
        #fetch the operation type
        optype = expr.operator.type
        #check whether the optype is recognised
        if optype == "Minus":
            self.checkNumber(expr.operator, right)
            #return the float value negated
            return -float(right)
        #check if a logical not
        elif optype == "Not":
            #return the not of the operand
            return not self.isTruthy(right)

        ##if we couldn't get the value
        return None

    #define a way of unpacking a binary expression
    def BinaryExpr(self, expr):
        #fetch the left
        left = self.evaluate(expr.left)
        #and the right
        right = self.evaluate(expr.right)
        #and the operator
        optype = expr.operator.type
        #check the optype
        if optype == "Greater":
            self.checkNumbers(expr.operator, left, right)
            #greater comparison
            return float(left) > float(right)
        if optype == "Less":
            self.checkNumbers(expr.operator, left, right)
            #greater comparison
            return float(left) < float(right)
        if optype == "NotEqual":
            #inequality comparison
            return not self.isEqual(left, right)
        if optype == "EqualEqual":
            #equality comparison
            return self.isEqual(left, right)
        if optype == "Minus":
            self.checkNumbers(expr.operator, left, right)
            #subtract if given
            return float(left) - float(right)
        elif optype == "Slash":
            self.checkNumbers(expr.operator, left, right)
            #divide if given
            return float(left) / float(right)
        elif optype == "Star":
            self.checkNumbers(expr.operator, left, right)
            #multiply if given
            return float(left) * float(right)
        elif optype == "Plus":
            #check if left and right are numbers:
            if (isinstance(left, int) or isinstance(left, float)) and (isinstance(right, int) or isinstance(right, float)):
                return float(left) + float(right)
            #check if they are strings to concatenate
            if isinstance(left, string) and isinstance(right, string):
                return str(left) + str(right)
            #if neither triggered, this is probably wrong
            raise RuntimeError(expr.operator.lexeme+" operator requires two numbers or two strings.")
        #if we can't evaluate it at all, return None
        return None

    #define a way of checking if an object is a number
    def checkNumber(self, operator, obj):
        #if it is a float or int, it passes
        if isinstance(obj, float) or isinstance(obj, int):
            return
        #if it's a string
        elif isinstance(obj, str):
            #test if it can be converted to a float
            try:
                float(obj)
                return
            except:
                pass
        #raise an error if not
        raise RuntimeError(operator.lexeme+" operator requires a number.")

    #define a way of checking if multiple objects are numbers
    def checkNumber(self, operator, *args):
        #loop through all provided arguments
        for operand in args:
            #if it is a float or int
            if isinstance(operand, float) or isinstance(operand, int):
                #jump to the next value
                continue
            #if it's a string
            if isinstance(operand, str):
                #test if it can be converted to a float
                try:
                    float(operand)
                    #if no errors, jump to the next value
                    continue
                except:
                    pass
            #if we get to here, throw an error
            raise RuntimeError(operator.lexeme+" operator requires numbers.")

    #define a way of checking if something is truthy
    def isTruthy(self, obj):
        #If the object is none, false
        if obj == None:
            return False
        #if the object is boolean, return that
        if isinstance(obj, bool):
            return obj
        #if the object is the number zero
        if obj == 0:
            return False
        #everything else is true
        return True

    #define a way of checking if two values are equal
    def isEqual(self, a, b):
        #if they are both null, return true
        if (a==None) and (b==None):
            return True
        #if only one is null, return false
        if a==None:
            return False
        #else return the python equality
        return a==b

    #define a way of sending the interpreter to the correct method
    def evaluate(self, expr):
        ##List of all supported expressions
        exprs = {"Binary": self.BinaryExpr,
                 "Grouping": self.GroupingExpr,
                 "Unary": self.UnaryExpr,}
        #fetch the class name of the expression provided
        exprName = expr.__class__.__name__
        #return the correct method and pass in own value
        return exprs[exprName](expr)
