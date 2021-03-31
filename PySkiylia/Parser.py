 #!/usr/bin/env python
"""Generates usable code from our tokens"""
#The gramar of Skiylia is encoded in the Parser Class
#base python functions
import os

#import our code
from AbstractSyntax import *
from Lexer import Lexer
import Tokens

#define the parser class
class Parser:
    #limit the number of arguments a function can utilise
    arglimit=255
    #use this test test if we are in a loop
    loopdepth=0
    #initialise
    def __init__(self, skiylia, tokens=[], primitives=[], workingdir="", imported=[]):
        #return a method for accessing the skiylia class
        self.skiylia = skiylia
        #set our parser position to zero
        self.current = 0
        #set the output list to empty
        self.final = []
        #set the tokens
        self.tokens = tokens
        #set the primitives
        self.primitives = primitives
        #define all of the tokens that can start a block (not a lot as of current)
        self.blockStart = ["Colon"]
        #define the current directory
        self.mydir = workingdir
        #and define a list of imported modules
        self.imported = imported

    #define a way of starting up the parser
    def parse(self):
        #start with an empty list
        stmt = []
        #while we have more sourcecode to parse
        while not self.atEnd():
            #compile the nex statement and add to the list
            stmt.append(self.declaration())
        #trim any Null AST nodes
        #stmt = [x for x in stmt if x!=None]
        #return all the statements
        #print()
        return stmt

    #define the declaration grammar
    def declaration(self):
        try:
            #if we found an explicit variable declaration
            if self.match("Var"):
                #declare the variable
                return self.varDeclaration()
            #return the statement after
            return self.statement()
        #if we encountered an error, try to return to coherent code
        except Exception as e:
            #fetch the token
            token = e.args[0][0]
            #and message
            message = e.args[0][1]
            #and location if given
            where = "RuntimeError"
            if len(e.args[0]) > 2:
                where = e.args[0][2]
            #and raise an error
            self.skiylia.error(token.line, token.char, message, where)
            #try to re-synchronise with the code
            self.synchronise()
            return None

    #define the statement grammar
    def statement(self):
        #if we see anything in the blockstart list (a Colon token currently)
        if self.match(*self.blockStart):
            #anything folowing a startblock character is the start of a new block
            return Block(self.block())
        #if an indentation follows something that isn't a block definer
        elif (self.checkindent() > 0) and (self.previous().type not in self.blockStart):
            raise SyntaxError([self.peek(), "Incorect indentation for statement", "Indentation"])
        #check for a module import
        elif self.match("Import"):
            return self.importdeclaration()
        #if the next token is an if
        elif self.match("If"):
            #compute the if statement
            return self.ifstatement()
        #if the next token is a for
        elif self.match("For"):
            #compute the for
            return self.forstatement()
        #if the next token is a while
        elif self.match("While"):
            #compute the while statement
            return self.whilestatement()
        #if we see a class identifier
        elif self.match("Class"):
            return self.classdeclaration()
        #if the next token is a function declaration
        elif self.match("Def"):
            return self.functiondeclaration("function")
        #if we are returning from a function
        elif self.match("Return"):
            #fetch the return
            return self.returnstatement()
        #if we see a break or continue
        elif self.match("Break", "Continue"):
            return self.interuptstmt()
        #check if the token matches a primitive, and shortcut to the call logic
        elif self.peek().lexeme in self.primitives:
            ptoken = self.peek()
            #fetch the primitive code
            callfunc = self.call()
            #make sure the primitive closes
            self.consume("Unbounded function.", "End")
            callfunc.token = ptoken
            #and return it
            return callfunc
        #else return an expression statement
        return self.expressionstatement()

    #define the import grammar
    def importdeclaration(self):
        #fetch the name of the module
        module = self.consume("Expect module name after 'import'.", "Identifier")
        #consume the final end token
        self.consume("Unbounded import declaration.", "End")
        fpath = "{}\{}.skiy".format(self.mydir, module.lexeme)
        #check the module being imported exists
        if module.lexeme in self.imported:
            print("Module already imported")
            pass
        elif os.path.isfile(fpath):
            self.imported.append(module.lexeme)
            #fetcht the contents of the other module
            with open(fpath, "r") as f:
                bytes = f.read()
            #Pass the sourcecode to a new lexer
            lexer = Lexer(self.skiylia, bytes, False)
            #and scan the sourcecode for tokens
            tokens = lexer.scanTokens()
            #create a parser object
            parser = Parser(self.skiylia, tokens, self.primitives, workingdir=self.mydir)
            #and parse the sourcecode
            source = parser.parse()
            #fetch all of the top level functions
            methods = [x for x in source if isinstance(x, Function) or isinstance(x, Class)]
            #create a module abstraction
            return Import(module, source, methods)
        else:
            #otherwise, throw an error
            raise SyntaxError([module, "Module with name '{}' cannot be found.".format(module.lexeme), "Import"])

    #define the if statement grammar
    def ifstatement(self):
        #fetch the if conditional
        condition = self.expression()
        #make sure we have semicolon grammar
        if not self.check(*self.blockStart):
            raise RuntimeError(self.error(self.peek(), "Expect ':' after if condition"))
        #fetch the code to execute if the condition is true
        thenbranch = self.statement()
        #set else and elifs to none by default
        elsebranch, elifs = None, []
        while self.check("Elif"):
            self.advance()
            elifcondition = self.expression()
            #make sure we have semicolon grammar
            if not self.check(*self.blockStart):
                raise RuntimeError(self.error(self.peek(), "Expect ':' after if condition"))
            elifbranch = self.statement()
            elifs.append([elifcondition, elifbranch])
        #if there is an else
        if self.match("Else"):
            #WILL NEED TO ADD Indentation code to check else probably
            #check for grammar
            if not self.check(*self.blockStart):
                raise RuntimeError(self.error(self.peek(), "Expect ':' after else clause"))
            #and return the else statement
            elsebranch = self.statement()
        #return the abstracted If statement
        return If(condition, thenbranch, elifs, elsebranch)

    #define the for loop grammar
    def forstatement(self):
        #increment the loop counter
        self.loopdepth+=1
        #fetch the increment variable
        if self.match("Var"):
            #if we see an explicit variable declaration, do that
            initialiser = self.varDeclaration("Where", "Do", "Colon")
            #as we consumed the last token, back up one
            self.current -=1
        else:
            #else assume it's an expression
            initialiser = self.expressionstatement()

        #condition
        condition = None
        #check it has not been ommited
        if self.match("Where"):
            #fetch the conditional
            condition = self.expression()

        #increment operator
        increment = None
        #check it has not been ommited
        if self.match("Do"):
            increment = self.expression()
        else:
            self.constructincremental(initialiser.name)
            increment = self.expression()

        #check for the colon grammar
        if not self.check(*self.blockStart):
            raise RuntimeError(self.error(self.peek(), "Expect ':' after for condition"))
        #fetch the body of the for loop
        body = self.statement()

        #desugar / deconstruct into a while
        #check if we have been given an increment operation
        if increment:
            #add the incremental to the end of the body, so it will be executed then
            body = Block([body, Expression(increment)])

        #check if we didn't have a conditional
        if not condition:
            #if none supplied, assume true
            condition = Literal(True)
        #construct the while loop from the conditional and body
        body = While(condition, body, increment!=None)

        #as we require an initialiser, wrap it into the body code
        body = Block([initialiser, body])

        #decrement the loop counter
        self.loopdepth-=1

        #return the for loop in its' fully deconstructed form
        return body

    #define the function declaration grammar
    def functiondeclaration(self, functype):
        #fetch the name of the function
        name = self.consume("Expect {} name.".format(functype), "Identifier")
        #check for the parentheses grammar
        self.consume("Expect '(' after {} declaration.".format(functype), "LeftParenthesis")
        #empty parameter list
        params = []
        #check for zero parameters given
        if not self.check("RightParenthesis"):
            #fetch the first param
            params.append(self.consume("Expect parameter name.", "Identifier"))
            #while there is another, parameter
            while self.match("Comma"):
                #if we overshot the argumet limit
                if len(params) >= self.arglimit:
                    #show an error
                    self.error(self.peek(), "Can't have more than {} parameters.".format(self.arglimit))
                #otherwise, add the parameter
                params.append(self.consume("Expect parameter name.", "Identifier"))
        #make sure parentheses are closed
        self.consume("Expect ')' after {}".format(functype), "RightParenthesis")
        #check the indentation
        if not self.check(*self.blockStart):
            #show an error
            raise RuntimeError(self.error(self.peek(), "Expect ':' after {} declaration".format(functype)))
        #fetch the body of the function
        body = self.statement()
        #and return the function
        return Function(name, params, body)

    #define the class grammar
    def classdeclaration(self):
        #fetch the name of the class
        name = self.consume("Expected a class name.", "Identifier")
        #check for a superclass
        superclass = None
        #if we have a parenthesis, we have a super class
        if self.match("LeftParenthesis"):
            #make sure we are given a superclass
            self.consume("Expect superclass name.", "Identifier")
            #fetch the class reference
            superclass = Variable(self.previous())
            #and ensure we have closed the parenthesis correctly
            self.consume("Expect ')' to follow superclass.", "RightParenthesis")
        #double check grammar
        if not self.check(*self.blockStart):
            #show an error
            raise RuntimeError(self.error(self.peek(), "Expect ':' after class declaration"))
        #and advance past the grammar marker
        self.advance()
        #fetch the indentation of the class
        myIndent = self.peek().indent
        #if we have an ending token
        if self.check("End"):
            #skip it
            self.advance()
        #empty methods initialiser
        methods=[]
        #keep checking for new methods until the indentation decreases
        while (not self.atEnd()) and (self.checkindent(myIndent) != -1):
            #if the user has a "def" token, skip past it.
            if self.check("Def"):
                self.advance()
            #keep adding statements while the class has more methods
            methods.append(self.functiondeclaration("method"))
            #check if we have cascading end tokens
            if self.check("End") and (self.checkindent(myIndent) != -1):
                self.advance()
        #return the class
        return Class(name, superclass, methods)

    #define the interuption (break/continue) grammar
    def interuptstmt(self):
        #fetch the keyword
        keyword = self.previous()
        if self.loopdepth == 0:
            self.error(keyword, "Cannot use {} outside of a loop.".format(keyword.lexeme))
        #and ensure there is nothing after it
        self.consume("Expressions cannot follow '{}'.".format(keyword.lexeme),"End")
        #check that the code is then deindented
        if not self.checkindent(keyword.indent)<0:
            raise SyntaxError([self.peek(), "Incorect indentation for return statement", "Indentation"])
        #create and return the abstraction
        return Interupt(keyword, keyword.type=="Continue")

    #define the return grammar
    def returnstatement(self):
        #fetch the "Return" token for error reporting
        keyword = self.previous()
        #return none by default
        value = None
        #check the return has not been terminated empty
        if not self.check("End"):
            value = self.expression()
        #make sure there is an ending attatched to the return
        self.consume("Unbounded return statement.", "End")
        #check that the code is then deindented
        if not self.checkindent(keyword.indent)<0:
            raise SyntaxError([self.peek(), "Incorect indentation for return statement", "Indentation"])
        #return the return... interesting
        return Return(keyword, value)

    #define the variable declaration grammar
    def varDeclaration(self, *Endings):
        #if the variable terminator is not defined, pass an end token
        if len(Endings) < 1:
            Endings=("End",)
        #fetch the variable name
        name = self.consume("Expect variable name.", "Identifier")
        #define it's initial value as null
        initial = Literal(0.0) #None
        #if there is an equals, set it
        if self.match("Equal"):
            #fetch the value
            initial = self.expression()
        #make sure the variable is bounded
        self.consume("Unbounded variable declaration.", *Endings)
        #return the variable abstraction
        return Var(name, initial)

    #define the while statement grammar
    def whilestatement(self):
        #increment the loop counter
        self.loopdepth+=1
        #fetch the while conditional
        condition = self.expression()
        #make sure we have semicolon grammar
        if not self.check(*self.blockStart):
            raise RuntimeError(self.error(self.peek(), "Expect ':' after while condition"))
        #fetch the body of the while loop
        body = self.statement()
        #decrement the loop counter
        self.loopdepth-=1
        #return the While abstraction
        return While(condition, body)

    #define the expression statement grammar
    def expressionstatement(self):
        #fetch the expression
        expr = self.expression()
        #consume the end token
        self.consume("Unbounded expression.", "End")
        #return the abstraction
        return Expression(expr)

    #define the block grammar
    def block(self):
        #initialise an empty statement array, and fetch the current indentation leve;
        statements, myIndent = [], self.peek().indent
        #if we have an ending token
        if self.check("End"):
            #skip it
            self.advance()
        #continue to search for new statements while we have more sourcecode, and the indentation does not decrease
        while (not self.atEnd()) and (self.checkindent(myIndent) != -1):
            #keep adding statements while the block is open
            statements.append(self.declaration())
            #check if we have cascading end tokens
            if self.check("End") and (self.checkindent(myIndent) != -1):
                self.advance()
        #return the statement array
        return statements

    #define the expression grammar
    def expression(self):
        #return an asignment
        return self.conditional()

    #define the conditional (ternary) operator
    def conditional(self):
        #fetch the first part
        expr = self.assignment()
        #if we have the start of a conditional
        if self.match("Question"):
            #the then branch
            thenBranch = self.expression()
            #check for grammar
            self.consume("Expect ':' after ternary operator", "Colon")
            #and set the type to ternary
            type = "T"
        #or the start of an elvis
        elif self.match("QColon"):
            type, thenBranch = "E", 0
        #or the start of a null coalescence
        elif self.match("QQuestion"):
            type, thenBranch = "N", 0
        #if nothing, return the expr
        else:
            return expr
        #all conditionals have an else, so fetch it
        elseBranch = self.conditional()
        #and fincally construct the conditional
        return Conditional(expr, thenBranch, elseBranch, type)

    #define the asignment gramar
    def assignment(self):
        #return the equality
        expr = self.logicalor()
        #if there is an equals after the identifier
        if self.match("Equal"):
            #fetch the variable name
            equals = self.previous()
            #fetch it's value
            value = self.assignment()
            #if it is a Variable type
            if isinstance(expr, Variable):
                name = expr.name
                #return the assignment
                return Assign(name, value)
            elif isinstance(expr, Get):
                return Set(expr.object, expr.name, value)
            #throw an error if not
            self.skiylia.error([equals, "Invalid assignment target."])
        #return the variable
        return expr

    #define the logical or grammar
    def logicalor(self):
        #grab the binaary operation
        return self.leftAssociative(self.logicalxor, "Or", ExprType=Logical)

    #define the logical xor grammar
    def logicalxor(self):
        #grab the binaary operation
        return self.leftAssociative(self.logicaland, "Xor", ExprType=Logical)

    #define the logical and grammar
    def logicaland(self):
        #grab the binaary operation
        return self.leftAssociative(self.equality, "And", ExprType=Logical)

    #define the equality gramar
    def equality(self):
        #grab the binaary operation
        return self.leftAssociative(self.comparison, "NEqual", "NEEqual", "NFuzequal", "EEqual", "EEEqual", "Fuzequal")

    #define the comparison grammar
    def comparison(self):
        #grab the binaary operation
        return self.leftAssociative(self.term, "Greater", "EGreater", "Less", "ELess")

    #define the term grammar
    def term(self):
        #grab the binaary operation
        return self.leftAssociative(self.factor, "Plus", "Minus")

    #define the factor grammar
    def factor(self):
        #grab the binaary operation
        return self.leftAssociative(self.unary, "Star", "Slash", "StStar")

    #shorthand code for all left associative binary operations
    def leftAssociative(self, operand, *operators, ExprType=Binary):
        #fetch the first term
        expr = operand()
        #loop through all comparison posibilities
        while self.match(*operators):
            #fetch the operator
            operator = self.previous()
            #fetch the term associated
            right = operand()
            #create a binary expression from this
            expr = ExprType(expr, operator, right)
        #return the expression
        return expr

    #define the unary grammar
    def unary(self):
        #this is right associative, so check first
        if self.match("Not", "Minus"):
            #fetch the operator
            operator = self.previous()
            #fetch the unary that might follow (as per our EBNF gramar)
            right = self.unary()
            #return the unary combination
            return Unary(operator, right)
        #check for prefix '++' and '--'.
        elif self.match("PPlus", "MMinus"):
            #fetch the operator
            operator = self.previous()
            #fetch the call that may follow
            right = self.call()
            #return the unary combination
            return Unary(operator, right)
        #otherwise return the literal
        return self.postfix()

    #define the postfix grammar
    def postfix(self):
        #this is right associative, so check first
        if self.checkNext("PPlus", "MMinus"):
            #fetch the call that comes before
            left = self.call()
            #fetch the operator
            operator = self.peek()
            #and move past the incremental operators
            self.advance()
            #return the unary combination
            return Unary(operator, left, True)
        #otherwise return the literal
        return self.call()

    #define the function that checks for the end of a call
    def finishCall(self, callee):
        #empty arguments list
        arguments = []
        #check we have arguments to parse
        if not self.check("RightParenthesis"):
            #append the first argument to our list
            arguments.append(self.expression())
            #while there is a comma
            while self.match("Comma"):
                #if we have seen more arguments than our limit
                if len(arguments) >= self.arglimit:
                    #show an error
                    self.error(self.peek(), "Can't have more than {} arguments.".format(self.arglimit))
                #fetch and append the next argument
                arguments.append(self.expression())
        #fetch the final parenthesis
        paren = self.consume("Expect ')' after arguments.", "RightParenthesis")
        #can't have a colon after a call
        '''if self.check("Colon") and self.checkNext("End"):
            self.advance()
            raise SyntaxError(self.error(self.previous(), "':' cannot follow function calls."))'''
        #return the function call
        return Call(callee, paren, arguments)

    #define the function call grammar
    def call(self):
        #fetch the literal in front
        expr = self.literal()
        #keep looping
        while True:
            #if we have an open parenthesis
            if self.match("LeftParenthesis"):
                #fetch the rest of the call
                expr = self.finishCall(expr)
            #if we have class properties to interact with
            elif self.match("Dot"):
                #fetch the name of the property
                name = self.consume("Expected property name afte '.'.", "Identifier")
                expr = Get(expr, name)
            else:
                #otherwise stop here
                break
        #return the call
        return expr

    def literal(self):
        #check if we have any known identifiers
        if self.match("False"):
            return Literal(False)
        #check if true
        elif self.match("True"):
            return Literal(True)
        #check if null
        elif self.match("Null"):
            return Literal(None)
        #check if a number or string
        elif self.match("Number", "String"):
            return Literal(self.previous().literal)
        #check if we have a "self"
        elif self.match("Self"):
            return Self(self.previous())
        #check if we have a 'super'
        elif self.match("Super"):
            keyword = self.previous()
            self.consume("Expect '.' after 'super'.", "Dot")
            method = self.consume("Expect superclass method.", "Identifier")
            return Super(keyword, method)
        #check if a variable is there
        elif self.match("Identifier"):
            return Variable(self.previous())
        #check if opening a parenthesis
        elif self.match("LeftParenthesis"):
            expr = self.expression()
            self.consume("Expect ')' after an expression.", "RightParenthesis")
            return Grouping(expr)
        #if we meet an end where we shouldn't
        elif self.match("End"):
            raise SyntaxError([self.previous(), "Unbounded object."])
        #and add some error detection for operations that require something before them'''
        if self.checkError():
            return None
        #if we found nothing, throw an error
        return self.error(self.peek(), "Expected an expression.")

    def checkError(self):
        a = "" #function to execute if we find an error
        #check if we have an equality
        if self.match("NEqual", "NEEqual", "NFuzequal", "EEqual", "EEEqual", "Fuzequal"):
            a = self.equality
        #or a comparison
        elif self.match("Greater", "EGreater", "Less", "ELess"):
            a = self.comparison
        #or an addition (a blank '-' is a unary operator as well)
        elif self.match("Plus"):
            a = self.term
        #and finally a factor
        elif self.match("Slash", "Star", "StStar"):
            a = self.factor
        #otherwise, return false, as we didn't encounter an erroneous left hand operation
        else:
            return False
        #show the user our error
        self.error(self.previous(), "Missing left-hand opperand before {}".format(self.previous().lexeme))
        #execute the erroneous function to show a message to the user
        a()
        #and return true, as we found an error
        return True

    def constructincremental(self, var):
        self.tokens.insert(self.current, Tokens.Token("PPlus", "++", None, var.line, var.char, var.indent))
        self.tokens.insert(self.current, var)

    #define a way of checking if a token is found, and consuming it
    def consume(self, errorMessage, *type):
        #if it's the token we want, return it
        if self.check(*type):
            return self.advance()
        #else show an error
        raise RuntimeError(self.error(self.peek(), errorMessage))
        #could include a raise here instead I guess?

    #define a way of checking if the current token is any of the supplied types
    def match(self, *args):
        #loop through all types given to the function
        for type in args:
            #check if the type matches
            if self.check(type):
                #advance and return true if it does
                self.advance()
                return True
        #return false if nothing matched
        return False

    #basically match, but only on a single token type
    def check(self, *expected):
        #if we've run off the end of the tokens
        if self.atEnd():
            #return false
            return False
        #else return if the token is one of the expected ones
        return self.peek().type in expected

    #basically match, but only on a single token type
    def checkNext(self, *expected):
        #if we've run off the end of the tokens
        if self.atEnd():
            #return false
            return False
        #else return if the token is one of the expected ones
        return self.peekNext().type in expected

    #define a way of fetching the next tokens
    def advance(self):
        #if we havent run off the end of the tokens
        if not self.atEnd():
            #increment the position
            self.current+=1
        #return the token we just jumped over
        return self.previous()

    #check if we have reached the end of file
    def atEnd(self):
        #return if the next token is EOF
        return self.peek().type == "EOF"

    #define a way of returning the current token, without moving the parser position
    def peek(self):
        #return the token at the current position
        return self.tokens[self.current]

    #define a way of returning the next token, without moving the parser position
    def peekNext(self):
        #if we're at the end of the file, return the EOF token
        if self.atEnd():
            return self.tokens[self.current]
        #else return the token at the next position
        return self.tokens[self.current + 1]

    #define a way of checking if the next token has a higher or lower indentation than the current one does
    def checkindent(self, thatIndent="", thisIndent=""):
        #fetch the current tokens indentation
        if not thisIndent:
            thisIndent = self.peek().indent
        #if the code has not supplied an indent value
        if not thatIndent:
            #fetch the previous token indentation
            thatIndent = self.previous().indent
        #return 1 if the indent increases, -1 if it decreases, and 0 if it remains the same
        return int(thisIndent - thatIndent)

    #same as peek, but with the previous token instead
    def previous(self):
        return self.tokens[self.current - 1]

    #define a way of showing errors to the user
    def error(self, token, message):
        #if we reached the end of the file, show an EOF error
        if token.type == "EOF":
            self.skiylia.error(token.line, token.char, message, "at end of file, Syntax")
        #otherwise show the user what the exact location and token was
        else:
            self.skiylia.error(token.line, token.char, message, "at '"+token.lexeme+"', Syntax")
        #and return our base Parse error
        return [token, message, "Parse"]

    #define a way of returning to execution if an error was encountered
    def synchronise(self):
        #go to the next token
        self.advance()
        #keep going until we get to the end
        while not self.atEnd():
            #check if we have exited the current indentation level
            if self.checkindent() == -1:
                #break the loop
                break
            #otherise, get the current token type
            thisToken = self.peek().type
            #if it is one of the token types that starts a statement, stop the loop
            if thisToken in ["Class", "Def", "End", "For", "If", "Return", "Var", "While"]:
                break
            #move past the token we just found
            self.advance()
