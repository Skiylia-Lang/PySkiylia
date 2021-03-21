 #!/usr/bin/env python
"""Generates a sequence of tokens from plaintext"""

#import our code
from AbstractSyntax import *

#A class that will hold miscellaneous help code
class misc:
    #define a way of checking if objects are numbers
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
            raise RuntimeError([operator,"operator requires a number."])

    #define a way of testing if one, but not both, of two objects can be represented as an integer
    def xorNumber(self, a, b):
    	out=[]
        #check the two values
    	for x in [a,b]:
    		try:
                #try converting to float
    			int(x)
                #if it worked, return true
    			out.append(True)
    		except:
                #otherwise return false
    			out.append(False)
        #return the xor, then whether each value is a string
    	return out[0] ^ out[1], out[0], out[1]

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

    #convert internal representation to user readible code
    def stringify(self, obj):
        #if none, show null
        if obj==None:
            return "null"
        elif obj==True:
            return "true"
        elif obj==False:
            return "false"
        #if it's a number
        if isinstance(obj, float) or isinstance(obj, int):
            #if it's an integer, cast to integer first
            if obj.is_integer():
                return str(int(obj))
            #else just return it
            return str(obj)
        #return the string of the object
        return str(obj)

#define the Interpreter class
class Interpreter(misc):
    ##initialise
    def __init__(self):
        #fetch the Skiylia class so we have access to it's functions
        from PySkiylia import Skiylia
        self.skiylia = Skiylia()

    #define the interpreter function
    def interpret(self, statements):
        #try to execute code, escape if error
        try:
            #loop through all statements provided
            for statement in statements:
                #evaluate each statement
                self.execute(statement)
        except Exception as e:
            #fetch the token
            token = e.args[0][0]
            #and message
            message = e.args[0][1]
            #and raise an error
            self.skiylia.error(token.line, token.char, message, "RuntimeError")

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
            self.checkNumber(expr.operator, left, right)
            #greater comparison
            return float(left) > float(right)
        if optype == "Less":
            self.checkNumber(expr.operator, left, right)
            #greater comparison
            return float(left) < float(right)
        if optype == "NotEqual":
            #inequality comparison
            return not self.isEqual(left, right)
        if optype == "EqualEqual":
            #equality comparison
            return self.isEqual(left, right)
        if optype == "Minus":
            self.checkNumber(expr.operator, left, right)
            #subtract if given
            return float(left) - float(right)
        elif optype == "Slash":
            self.checkNumber(expr.operator, left, right)
            #divide if given
            if float(right) == 0:
                raise RuntimeError([expr.operator,"division by zero"])
            return float(left) / float(right)
        elif optype == "Star":
            #check if one (and only one) is a number, so we can repeat substrings
            xornum = self.xorNumber(left, right)
            #if only one is
            if xornum[0]:
                #if left is a number
                if xornum[1]:
                    #repeat the right string (Python requires integers for string multiplication)
                    return int(left) * right
                #otherwise repeat the left string
                return right * int(left)
            #check they can both be converted to numbers
            self.checkNumber(expr.operator, left, right)
            #multiply if given
            return float(left) * float(right)
        elif optype == "Plus":
            #check if either is a strings to concatenate
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            #otherwise check if they are numberable
            self.checkNumber(expr.operator, left, right)
            #compute calculation if all went well
            return float(left) + float(right)
            #if neither triggered, this is probably wrong
        #if we can't evaluate it at all, return None
        return None

    #define the way of interpreting an expression statement
    def ExpressionStmt(self, stmt):
        #evaluate the expression
        self.evaluate(stmt.expression)
        #and return none
        return None

    #define the way of interpreting a print statement
    def PrintStmt(self, stmt):
        #evaluate the expression
        value = self.evaluate(stmt.expression)
        #print the output
        print(self.stringify(value))
        #and return none
        return None

    #define a way of sending the interpreter to the correct expression method
    def evaluate(self, expr):
        ##List of all supported expressions
        exprs = {"Binary": self.BinaryExpr,
                 "Grouping": self.GroupingExpr,
                 "Literal": self.LiteralExpr,
                 "Unary": self.UnaryExpr,}
        #fetch the class name of the expression provided
        exprName = expr.__class__.__name__
        #return the correct method and pass in own value
        return exprs[exprName](expr)


    #define a way of sending the interpreter to the correct statement method
    def execute(self, stmt):
        ##List of all supported expressions
        stmts = {"Expression": self.ExpressionStmt,
                 "Print": self.PrintStmt,}
        #fetch the class name of the expression provided
        stmtName = stmt.__class__.__name__
        #return the correct method and pass in own value
        return stmts[stmtName](stmt)
