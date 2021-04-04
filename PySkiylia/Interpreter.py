 #!/usr/bin/env python
"""Executes code from Abstractions"""

#import our code
from Environment import Environment
from ASTPrinter import Evaluator
from SkiyliaCallable import *
from AbstractSyntax import *
import Primitives

#A class that will hold miscellaneous help code
class misc:
    stringify = Primitives.stringify
    #define a way of checking if objects are numbers
    def checkNumber(self, operator, *args):
        #loop through all provided arguments
        for operand in args:
            #if it is a float or int
            if isinstance(operand, (float, int)):
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
                    raise RuntimeError([operator,"'{}' not valid for '{}' operator, requires a number.".format(operand, operator.lexeme)])
            #if we get to here, throw an error
            raise RuntimeError([operator,"'{}' not valid for '{}' operator, requires a number.".format(operand, operator.lexeme)])

    #convert an object to an integer where possible
    def intifpos(self, operand):
        if isinstance(operand, int):
            return operand
        try:
            op = float(operand)
            if op.is_integer():
                return int(op)
            return op
        except:
            return operand

    #define a way of testing if one, but not both, of two objects can be represented as an integer
    def xorNumber(self, a, b):
    	out=[]
        #check the two values
    	for x in [a,b]:
    		try:
                #try converting to float
    			float(x)
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
        if obj is None:
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
        #if they are both null, return true, if only one is, return false
        if (a is None):
            return b is None
        try:
            #check for equivalent valuation, if not equivalent typing
            return float(a) == float(b)
        except:
            #else return the python equality
            return a==b

#define the Interpreter class
class Interpreter(misc, Evaluator):
    ##initialise
    def __init__(self, skiylia, arglimit, workingdir=""):
        #return a method for accessing the skiylia class
        self.skiylia = skiylia
        #track the current global environment scope
        self.globals = Environment()
        #and a our current variable scope
        self.environment = self.globals
        #define the locals dictionary
        self.locals = dict()
        #define the maximum number of allowed arguments in a function call
        self.arglimit = arglimit
        #define our current working directory
        self.mydir = workingdir
        #define a way of skipping to the last part of a block
        self.skipToLast = False
        #and add our primitives to the global scope
        self.primitives = []
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
                self.primitives.append(callname)
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
            #default error type, if none given
            where = "Runtime"
            try:
                where = e.args[0][2]
            except:
                where = "Runtime"
            #and raise an error
            self.skiylia.error(token.line, token.char, message, where)

    #define a way to assign variables abstractly
    def AssignExpr(self, expr):
        #evaluate what should be assignd
        value = self.evaluate(expr.value)
        #fetch the distance to the variable
        try:
            dist = self.locals[expr]
        except:
            dist = None
        #if there was one,
        if dist:
            #assign it in that environment
            self.environment.assignAt(dist, expr.name.lexeme, value)
        else:
            #otherwise, add to globals
            self.globals.define(expr.name, value)
        return value

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
        elif optype == "EGreater":
            self.checkNumber(expr.operator, left, right)
            #greater or equal comparison
            return float(left) >= float(right)
        elif optype == "Less":
            self.checkNumber(expr.operator, left, right)
            #less comparison
            return float(left) < float(right)
        elif optype == "ELess":
            self.checkNumber(expr.operator, left, right)
            #less of equal comparison
            return float(left) <= float(right)
        elif optype == "NEqual":
            #inequality comparison
            return not self.isEqual(left, right)
        elif optype == "EEqual":
            #equality comparison
            return self.isEqual(left, right)
        elif optype == "NEEqual":
            #strictly not equal
            if isinstance(left, type(right)) and self.isEqual(left, right):
                #if they're the same type, and are equal, return false
                return False
            #true in any other case
            return True
        elif optype == "EEEqual":
            #strictly equal
            if isinstance(left, type(right)):
                #if they're the same type, check if they are equal
                return self.isEqual(left, right)
            #false if they have different types
            return False
        elif optype == "NFuzequal":
            #Fuzzily equal only checks for type equality
            return not isinstance(left, type(right))
        elif optype == "Fuzequal":
            #Fuzzily equal only checks for type equality
            return isinstance(left, type(right))
        elif optype == "Minus":
            self.checkNumber(expr.operator, left, right)
            #subtract if given
            return self.intifpos(float(left) - float(right))
        elif optype == "Slash":
            self.checkNumber(expr.operator, left, right)
            #divide if given
            if float(right) == 0:
                raise RuntimeError([expr.operator,"division by zero"])
            return self.intifpos(float(left) / float(right))
        elif optype == "StStar":
            self.checkNumber(expr.operator, left, right)
            return self.intifpos(float(left) ** float(right))
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
            return self.intifpos(float(left) * float(right))
        elif optype == "Plus":
            #check if either is a strings to concatenate
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            #otherwise check if they are numberable
            self.checkNumber(expr.operator, left, right)
            #compute calculation if all went well
            return self.intifpos(float(left) + float(right))
            #if neither triggered, this is probably wrong

    #define the methods for dealing with block abstractions
    def BlockStmt(self, stmt):
        #execute the next block, passing in the statements and creating a new environment
        self.executeBlock(stmt.statements, Environment(self.environment))

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
        if expr.callee.name.lexeme in self.primitives:
            return self.intifpos(callee.call(self, args, expr.callee.name))
        return self.intifpos(callee.call(self, args, expr.callee.name))

    #define how our interpreter handles classes
    def ClassStmt(self, stmt):
        #check for the superclass
        superclass = None
        if stmt.superclass:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, SkiyliaClass):
                raise RuntimeError([stmt.superclass.name, "Superclass must be a class."])
        #ensure the class is defined in our environment
        self.environment.define(stmt.name.lexeme, None)
        #and add the definition of "super" in our scope
        if stmt.superclass:
            #create a new scope for the super
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)
        #deal with the methods of the class
        methods = dict()
        #iterate through all the methods
        for method in stmt.methods:
            #create a new function instance, making sure that we set "isinit" to true if this method is the init one
            function = SkiyliaFunction(method, self.environment, method.name.lexeme=="init")
            #and set it within our methods dictionary
            methods[method.name.lexeme] = function
        #create a new class object with superclass
        thisclass = SkiyliaClass(stmt.name.lexeme, superclass, methods)
        #escape out of the superclass scope if we made one
        if stmt.superclass:
            #create a new scope for the super
            self.environment = self.environment.enclosing
        #and assign it the pointer created above
        self.environment.assign(stmt.name, thisclass)
        #and return none by default
        return thisclass

    #define the way of interpreting a conditional statement
    def ConditionalStmt(self, stmt):
        #evaluate the conditional
        cond = self.evaluate(stmt.condition)
        #fetch the conditional type
        contype = stmt.type
        #check if we have null and a null coalescence conditional
        if (contype=="N"):
            #unless conditional is explicitly null
            if cond is not None:
                #return it
                return cond
            #otherwise, execute the else branch
            return self.evaluate(stmt.elseBranch)
        #otherwise, evaluate the truthiness of the if condition
        elif self.isTruthy(cond):
            #if the conditional is ternary:
            if contype == "T":
                #evaluate the 'then'
                return self.evaluate(stmt.thenBranch)
            #otherwise, its an elvis, so just return the condition
            return cond
        #otherwise, execute the else branch
        return self.evaluate(stmt.elseBranch)

    #define the way of interpreting an expression statement
    def ExpressionStmt(self, stmt):
        #evaluate the expression
        self.evaluate(stmt.expression)

    #define the way of interpreting a function
    def FunctionStmt(self, stmt):
        #create the function object
        function = SkiyliaFunction(stmt, self.environment)
        #add it to the environment
        self.environment.define(stmt.name.lexeme, function)
        #and return None by default
        return function

    #define the way of interpreting an if statement
    def IfStmt(self, stmt):
        #evaluate the truthiness of the if condition
        if self.isTruthy(self.evaluate(stmt.condition)):
            #if true, execute
            self.evaluate(stmt.thenBranch)
        #check all the elifbranches
        for x in stmt.elseifs:
            #if this elif
            if self.isTruthy(self.evaluate(x[0])):
                #evaluate and stop checking
                self.evaluate(x[1])
                break
        #this else will only execute if the break never called
        else:
            if stmt.elseBranch:
                #execute it
                self.evaluate(stmt.elseBranch)

    #define a way of handling an imported module
    def ImportStmt(self, stmt):
        #define the module in the interpreter globals
        self.globals.define(stmt.name.lexeme, None)
        #define all of the accessible functions and classes in this module
        methods = dict()
        #iterate through all the methods
        for method in stmt.methods:
            #create functions for each of the module methods
            function = self.evaluate(method) #SkiyliaFunction(method, self.globals, method.name.lexeme=="init")
            #and set it within our methods dictionary
            methods[method.name.lexeme] = function
        #create a new module object
        module = SkiyliaModule(stmt.name.lexeme, methods)
        #and return the instantiated module
        module = module.instance
        #and assign this module to the environment
        self.globals.assign(stmt.name, module)

    #define a way of using an interup (continue/break)
    def Interuptstmt(self, stmt):
        #raise an error
        raise Interupt(stmt.cont)

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
                return not self.isTruthy(self.evaluate(expr.right))
        #evaluate the right operand if nothing else
        return self.isTruthy(self.evaluate(expr.right))

    def GetExpr(self, expr):
        #fetch the object being refered to
        obj = self.evaluate(expr.object)
        #if the object is an instance
        if isinstance(obj, SkiyliaInstance):
            #return the properties of the ibject
            return obj.get(expr.name)
        #throw an error if not
        raise RuntimeError([expr.name, "Only instances have properties."])

    #define a way of unpacking a grouped expression at runtime
    def GroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    #define the return grammar
    def ReturnStmt(self, stmt):
        #none by default
        value = None
        #if we have a value
        if stmt.value:
            #evaluate it
            value = self.evaluate(stmt.value)
        #create an exception so we can return all the way back to the call
        raise Return(value)

    #self grammar
    def SelfExpr(self, expr):
        #return the keyword from variable
        return self.lookupvariable(expr.keyword, expr)

    def SetExpr(self, expr):
        #get the object this is refering to
        obj = self.evaluate(expr.object)
        #if the object is not a skiylia instance
        if not isinstance(obj, SkiyliaInstance):
            raise RuntimeError([expr.name, "Only instances have fields."])
        #fetch the value that is to be set
        value = self.evaluate(expr.value)
        #and set the instance property
        obj.set(expr.name, value)
        #and return the value that was set
        return value

    #define the superclass stuff!
    def SuperExpr(self, expr):
        #fetch the distance to the superclass
        dist = self.locals[expr]
        #and retrun the actual reference to it
        superclass = self.environment.getAt(dist, "super")
        #return the reference to the class calling it's super
        obj = self.environment.getAt(dist - 1, "self")
        #and get the method being called
        method = superclass.findMethod(expr.method.lexeme)
        #if the method doesn't exist
        if not method:
            #throw an error
            raise RuntimeError([expr.method, "Undefined property '{}'.".format(expr.method.lexeme)])
        #return the method, bound to the child class
        return method.bind(obj)

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
            return -self.intifpos(right)
        #check if a logical not
        elif optype == "Not":
            #return the not of the operand
            return not self.isTruthy(right)
        #check if it is an incremental
        elif optype == "PPlus":
            #ensure the operator is a number we can increment
            self.checkNumber(expr.operator, right)
            #fetch the value of the operand
            value = self.intifpos(right)
            #check if the operand is a variable
            if isinstance(expr.right, Variable):
                var = self.VarExpr(expr.right)
                #and update it if it was
                self.environment.assign(expr.right.name, value + 1)
            #if the operator was in postfix
            if expr.postfix:
                #return the original value
                return value
            #otherwise return the value + 1
            return value + 1
        #check if it is an decremental
        elif optype == "MMinus":
            #ensure the operator is a number we can decrement
            self.checkNumber(expr.operator, right)
            #fetch the value of the operand
            value = self.intifpos(right)
            #check if the operand is a variable
            if isinstance(expr.right, Variable):
                var = self.VarExpr(expr.right)
                #and update it if it was
                self.environment.assign(expr.right.name, value - 1)
            #if the operator was in postfix
            if expr.postfix:
                #return the original value
                return value
            #otherwise return the value - 1
            return value - 1

    #define the method of fetching a variables value
    def VarExpr(self, expr):
        #fetch the name from the Environment holder
        return self.lookupvariable(expr.name, expr)

    #define the ways of handling variables
    def VarStmt(self, stmt):
        #define the default value
        value = None
        #if the variable has an initial value assigned
        if stmt.initial:
            #evaluate and return the initial value
            value = self.intifpos(self.evaluate(stmt.initial))
        #store the variable in our environment
        self.environment.define(stmt.name.lexeme, value)

    #define how we handle the while abstraction
    def WhileStmt(self, stmt):
        #while the condition is truthy
        while self.isTruthy(self.evaluate(stmt.condition)):
            try:
                #execute the body of the while loop
                self.evaluate(stmt.body)
            #if we got an interupt command
            except Interupt as e:
                #if the intreuption is continue
                if e.message is True:
                    #if the loop contains an incremental
                    if stmt.hasincrement:
                        #try to execute it (it will always be the last thing in the while block)
                        self.skipToLast = True
                        self.evaluate(stmt.body)
                    #now it will redo the loop
                else:
                    #otherwise, break
                    break

    #define a way of executing block code
    def executeBlock(self, statements, environment):
        #store the parent environment
        previous = self.environment
        try:
            #make sure the current scope is the one to compute with
            self.environment = environment
            #check if we only want to execute the last part of the block
            if not self.skipToLast:
                #loop through the given statements
                for statement in statements:
                    #and execute them
                    self.evaluate(statement)
            else:
                #reset the skip flag
                self.skipToLast = False
                #and evaluate the last part of the block
                self.evaluate(statements[-1])
        finally:
            #restore the parent scope now we have finished
            self.environment = previous

    #define a way of reoslving local names
    def resolve(self, expr, depth):
        #store the expression and depth
        self.locals[expr] = depth

    #define a way of searching for a variable given environment depth
    def lookupvariable(self, name, expr):
        try:
            #fetch the distance up the scope
            dist = self.locals[expr]
        except:
            dist = None
        #if we have a dist
        if dist is not None:
            #then fetch from there
            return self.environment.getAt(dist, name.lexeme)
        #otherwise we have a global
        return self.globals.fetch(name)
