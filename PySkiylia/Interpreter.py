 #!/usr/bin/env python
"""Executes code from Abstractions"""

#import our code
from AbstractSyntax import *
from Environment import Environment
from SkiyliaCallable import SkiyliaCallable
import Primitives

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
            raise RuntimeError([operator,"'"+operator.lexeme+"' operator requires a number."])

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
        #if the object is boolean
        elif isinstance(obj, bool):
            #if the object is true
            if obj==True:
                return "true"
            #else the object is false
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
    def __init__(self, skiylia, arglimit):
        #return a method for accessing the skiylia class
        self.skiylia = skiylia
        #track the current global environment scope
        self.globals = Environment()
        #and a our current variable scope
        self.environment = self.globals
        #define the maximum number of allowed arguments in a function call
        self.arglimit = arglimit
        #and add our primitives to the global scope
        self.fetchprimitives()

    #define the primitives
    def fetchprimitives(self):
        #fetch all classes who are a subclass of SkiyliaCallable
        primitives = SkiyliaCallable.__subclasses__()
        #itterate through them
        for primitive in primitives:
            #if they are from the primitives module
            if primitive.__module__ == "Primitives":
                #fetch the call name
                callname = primitive.__name__
                #check if a custom one has been defined
                if primitive.callname:
                    callname=primitive.callname
                #add them to the global scope
                self.globals.define(callname, primitive())

    #define the interpreter function
    def interpret(self, statements):
        #try to execute code, escape if error
        try:
            #loop through all statements provided
            for statement in statements:
                #evaluate each statement
                self.evaluate(statement)
        except Exception as e:
            #fetch the token
            token = e.args[0][0]
            #and message
            message = e.args[0][1]
            #and raise an error
            self.skiylia.error(token.line, token.char, message, "Runtime")

    #define a way to assign variables abstractly
    def AssignExpr(self, expr):
        #evaluate what should be assignd
        value = self.evaluate(expr.value)
        #add that to the environment storage
        self.environment.assign(expr.name, value)
        #and return the value
        return value

    #define a way of converting from the literal AST to a runtime value
    def LiteralExpr(self, expr):
        return expr.value

    #define a way of unpacking abstracted Logicals
    def LogicalExpr(self, expr):
        #fetch the left
        left = self.evaluate(expr.left)
        #as 'or' will be true if left is true, and 'and' will be false is left is false, we can short circuit the logical
        if expr.operator.type == "Or":
            #if left is true, 'or' will be true
            if self.isTruthy(left):
                return left
        elif expr.operator.type == "And":
            #if left is false, 'and' will be false
            if not self.isTruthy(left):
                return left
        elif expr.operator.type == "Xor":
            #if left is true, 'xor' will be the opposite of right
            if self.isTruthy(left):
                return not self.evaluate(expr.right)

        return self.evaluate(expr.right)

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

    #define a way of performing a call
    def CallExpr(self, expr):
        #fetch the function name
        callee = self.evaluate(expr.callee)
        #empty args list
        args=[]
        #if we have arguments, loop through them
        for arg in expr.arguments:
            #append each argument to the list
            args.append(self.evaluate(arg))
        #check the callee is actually callable
        if not isinstance(callee, SkiyliaCallable):
            #throw an error if it's not a callable object
            raise RuntimeError([expr.parenthesis, "Can only call functions and classes"])
        if isinstance(callee.arity, str):
            minargs, maxargs = [int(x.replace("*", str(self.arglimit))) for x in callee.arity.split(",")]
            arglim = str(minargs)+" to "+str(maxargs)
        else:
            minargs = maxargs = arglim = callee.arity
        #check we have been given the correct number of arguments
        if not (minargs <= len(args) <= maxargs):
            #raise an error if it was different
            raise RuntimeError([expr.parenthesis, "Expected {} argument{} but got {}.".format(arglim, "s"*(arglim!=1), len(args))])
        #return and call the callable
        return callee.call(self, args)

    #define the method of fetching a variables value
    def VarExpr(self, expr):
        #fetch the name from the Environment holder
        return self.environment.fetch(expr.name)

    #define the methods for dealing with block abstractions
    def BlockStmt(self, stmt):
        #execute the next block, passing in the statements and creating a new environment
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    #define the way of interpreting an expression statement
    def ExpressionStmt(self, stmt):
        #evaluate the expression
        self.evaluate(stmt.expression)
        #and return none
        return None

    #define the way of interpreting an if statement
    def IfStmt(self, stmt):
        #evaluate the truthiness of the if condition
        if self.isTruthy(self.evaluate(stmt.condition)):
            #if true, execute
            self.evaluate(stmt.thenBranch)
        #if false, and we have an else branch
        elif stmt.elseBranch != None:
            #execute it
            self.evaluate(stmt.elseBranch)
        return None

    '''#define the way of interpreting a print statement
    def PrintStmt(self, stmt):
        #evaluate the expression
        value = self.evaluate(stmt.expression)
        #print the output
        print(self.stringify(value))
        #and return none
        return None'''

    #define the ways of handling variables
    def VarStmt(self, stmt):
        #define the default value
        value = None
        #if the variable has an initial value assigned
        if stmt.initial != None:
            #evaluate and return the initial value
            value = self.evaluate(stmt.initial)
        #store the variable in our environment
        self.environment.define(stmt.name.lexeme, value)
        #and return none
        return None

    #define how we handle the while abstraction
    def WhileStmt(self, stmt):
        #while the condition is truthy
        while self.isTruthy(self.evaluate(stmt.condition)):
            #execute the body of the while loop
            self.evaluate(stmt.body)
        #and return none
        return None

    #define a way of sending the interpreter to the correct method
    def evaluate(self, abstract):
        ##List of all supported expressions and statements
        abstracts = {"Assign":self.AssignExpr,
                     "Binary": self.BinaryExpr,
                     "Call": self.CallExpr,
                     "Grouping": self.GroupingExpr,
                     "Logical": self.LogicalExpr,
                     "Literal": self.LiteralExpr,
                     "Unary": self.UnaryExpr,
                     "Variable": self.VarExpr,
                     "Block": self.BlockStmt,
                     "Expression": self.ExpressionStmt,
                     "If": self.IfStmt,
                     #"Print": self.PrintStmt,
                     "Var":self.VarStmt,
                     "While":self.WhileStmt,}
        #fetch the class name of the abstract provided
        abstractName = abstract.__class__.__name__
        #return the correct method and pass in own value
        return abstracts[abstractName](abstract)

    #define a way of executing block code
    def executeBlock(self, statements, environment):
        #store the parent environment
        previous = environment
        try:
            #make sure the current scope is the one to compute with
            self.environment = environment
            #loop through the given statements
            for statement in statements:
                #and execute them
                self.evaluate(statement)
        finally:
            #restore the parent scope now we have finished
            self.environment = previous
