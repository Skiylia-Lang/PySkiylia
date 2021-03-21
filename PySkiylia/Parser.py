 #!/usr/bin/env python
"""Generates usable code from our tokens"""
#The gramar of Skiylia is encoded in the Parser Class

#import our code
from AbstractSyntax import *
import Tokens

#define the parser class
class Parser:
    #initialise
    def __init__(self, tokens=[]):
        #fetch the Skiylia class so we have access to it's functions
        from PySkiylia import Skiylia
        self.skiylia = Skiylia()
        #set our parser position to zero
        self.current = 0
        #set the output list to empty
        self.final = []
        #set the tokens
        self.tokens = tokens

    #define a way of starting up the parser
    def parse(self):
        #start with an empty list
        stmnt = []
        #while we have more sourcecode to parse
        while not self.atEnd():
            #compile the nex statement and add to the list
            stmnt.append(self.declaration())
        #return all the statements
        return stmnt

    #define the declaration grammar
    def declaration(self):
        try:
            #if we found an explicit variable declaration
            if self.match("Var"):
                #declare the variable
                return self.varDeclaration(Explicit=True)
            #return the statement after
            return self.statement()
        #if we encountered an error, try to return to coherent code
        except Exception as e:
            print(e)
            self.synchronise()
            return None

    #define the statement grammar
    def statement(self):
        #if the user has used multiple newlines, discard them
        while self.match("End"):
            pass
        #if the next token is a print
        if self.match("Print"):
            #compute the print statement
            return self.printstatement()
        #else return an expression statement
        return self.expressionstatement()

    #define the print statement grammar
    def printstatement(self):
        #ensure we have brackets
        self.consume("LeftParenthesis", "Expect '(' after print.")
        #fetch the enclosed expression
        value = self.expression()
        #ensure we have brackets
        self.consume("RightParenthesis", "Expect ')' after print.")
        #the print statement must also be bound
        self.consume("End", "Unbounded expression.")
        #return the abstract for print
        return Print(value)

    #define the variable declaration grammar
    def varDeclaration(self, Explicit=False):
        #fetch the variable name
        name = self.consume("Identifier", "Expect variable name.")
        #define it's initial value as null
        initial = None
        #if this is an implicit declaration
        if not Explicit:
            #then we require a value to equate to
            self.consume("Equal", "Value required for implicit variable declaration")
            #fetch the value
            initial = self.expression()
        #otherwise this is an explicit declaration
        else:
            #if there is an equals, set it
            if self.match("Equal"):
                #fetch the value
                initial = self.expression()
        #make sure the variable is bounded
        self.consume("End", "Unbounded variable declaration.")
        #return the variable abstraction
        return Var(name, initial)

    #define the expression statement grammar
    def expressionstatement(self):
        #fetch the expression
        expr = self.expression()
        #consume the end token
        self.consume("End", "Unbounded expression.")
        #return the abstraction
        return Expression(expr)

    #define the expression grammar
    def expression(self):
        #define the first comparitive term
        expr = self.comparison()
        #loop the other possible terms in the equality
        while self.match("NotEqual", "EqualEqual"):
            #fetch the operator, which should be the previous token
            operator = self.previous()
            #fetch the comparisonassociated
            right = self.comparison()
            #create a binary expression from this
            expr = Binary(expr, operator, right)
        #return the expression
        return expr

    #define the comparison grammar
    def comparison(self):
        #fetch the first term
        expr = self.term()
        #loop through all comparison posibilities
        while self.match("Greater", "Less"):
            #fetch the operator
            operator = self.previous()
            #fetch the term associated
            right = self.term()
            #create a binary expression from this
            expr = Binary(expr, operator, right)
        #return the comparison
        return expr

    #define the term grammar
    def term(self):
        #fetch the first factor
        expr = self.factor()
        #loop through all comparison posibilities
        while self.match("Plus", "Minus"):
            #fetch the operator
            operator = self.previous()
            #fetch the factir associated
            right = self.factor()
            #create a binary expression from this
            expr = Binary(expr, operator, right)
        #return the comparison
        return expr

    #define the factor grammar
    def factor(self):
        #fetch the first factor
        expr = self.unary()
        #loop through all comparison posibilities
        while self.match("Star", "Slash"):
            #fetch the operator
            operator = self.previous()
            #fetch the unary associated
            right = self.unary()
            #create a binary expression from this
            expr = Binary(expr, operator, right)
        #return the comparison
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
        #otherwise return the literal
        return self.literal()

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
        #check if a variable is there
        elif self.match("Idenitifer"):
            #if it is followed by an equals, this is an implicit declaration
            if self.peek("Equal"):
                #if it an implicit declaration, backup and declare it
                self.current-=1
                return self.varDeclaration()
            #otherwise it's just the code using the variable
            else:
                return Variable(self.previous())
        #check if opening a parenthesis
        elif self.match("LeftParenthesis"):
            expr = self.expression()
            self.consume("RightParenthesis", "Expect ')' after an expression.")
            return Grouping(expr)
        elif self.match("End"):
            pass
        #if we found nothing, throw an error
        return self.error(self.peek(), "Expected an expression.")

    #define a way of checking if a token is found, and consuming it
    def consume(self, type, errorMessage):
        #if it's the token we want, return it
        if self.check(type):
            return self.advance()
        #else show an error
        raise RuntimeError(self.error(self.peek, errorMessage))
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
    def check(self, expected):
        #if we've run off the end of the tokens
        if self.atEnd():
            #return false
            return False
        #else return if the token is the expected one
        return self.peek().type == expected

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

    #same as peek, but with the previous token instead
    def previous(self):
        return self.tokens[self.current - 1]

    #define a way of showing errors to the user
    def error(self, token, message):
        #if we reached the end of the file, show an EOF error
        if token.type == "EOF":
            self.skiylia.error(token.line, token.char, message, "at end of file")
        #otherwise show the user what the exact location and token was
        else:
            self.skiylia.error(token.line, token.char, message, "at '"+token.lexeme+"'")
        #and return our base Parse error
        return "Parse error: "+message

    #define a way of returning to execution if an error was encountered
    def synchronise(self):
        #go to the next token
        self.advance()
        #keep going until we get to the end
        while not self.atEnd():
            #check if we have found a statement ending token (newline)
            if self.previous().type == "End":
                #break the loop
                break
            #otherise, get the current token type
            thisToken = self.peek().type
            #if it is one of the token types that starts a statement, stop the loop
            if thisToken in ["Class", "Def", "Var", "For", "If", "While", "Print", "Return"]:
                break
        #move past the token we just found
        self.advance()
